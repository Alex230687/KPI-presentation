from copy import deepcopy
from pandas import Series
from django_pandas.io import read_frame
from main.models import Report, Target, Indicator, Data, DataType


class BaseQueryManager:
    def __init__(self):
        self.query = dict.fromkeys(['row', 'branch', 'forecast', 'target', 'indicator'])
        self.manager_chain = [self.row_query, self.branch_query, self.forecast_query, self.target_query,
                              self.indicator_query]

    def row_query(self, kwargs):
        """Get row id list for current indicator."""
        if self.query['row'] is None:
            self.query['row'] = Report.objects.filter(
                indicator=kwargs['indicator'], year=kwargs['year'], row_code__isnull=False
                ).order_by('row_position').values_list('row_code', flat=True)

    def branch_query(self, kwargs):
        """Get organization id list for current indicator."""
        if self.query['branch'] is None:
            if kwargs['branch'] == 6:
                self.query['branch'] = Report.objects.filter(
                    indicator=kwargs['indicator'], year=kwargs['year'], org_code__isnull=False
                    ).values_list('org_code', flat=True)
            else:
                self.query['branch'] = Report.objects.filter(
                    indicator=kwargs['indicator'], year=kwargs['year'], org_code=kwargs['branch']
                    ).values_list('org_code', flat=True)

    def forecast_query(self, kwargs):
        """Get datatype id list for current forecast method (get from web-form)."""
        if self.query['forecast'] is None:
            if kwargs['forecast'] == 2:
                self.query['forecast'] = DataType.objects.filter(id__in=[1, 2, 3]) \
                    .values_list('name', flat=True)
            elif kwargs['forecast'] == 3:
                self.query['forecast'] = DataType.objects.filter(id__in=[1, 2, 4]) \
                    .values_list('name', flat=True)
            else:
                self.query['forecast'] = DataType.objects.filter(id__in=[1, 2]) \
                    .values_list('name', flat=True)

    def target_query(self, kwargs):
        """Get special target value (if return 0 then use budget data)."""
        if self.query['target'] is None:
            self.query['target'] = Target.objects.filter(indicator=kwargs['indicator'], year=kwargs['year']) \
                .values_list('target', flat=True)[0]

    def indicator_query(self, kwargs):
        """Get indicator information."""
        if self.query['indicator'] is None:
            self.query['indicator'] = Indicator.objects.filter(id=kwargs['indicator']) \
                .select_related('indicator_group', 'indicator_effect') \
                .values('id', 'name', 'indicator_group__name', 'indicator_effect__name')[0]

    def run_query_manager(self, kwargs):
        for method in self.manager_chain:
            method(kwargs)


class BaseDataManager:
    REPORT_RF = ('indicator', 'indicator__indicator_group', 'indicator__indicator_effect')
    REPORT_VF = ('row_code', 'indicator__id', 'row_position', 'numerator', 'denominator')
    DATA_RF = ('row', 'data_type', 'row__row_type', 'row__row_group1', 'row__row_group2', 'row__row_group3')
    DATA_VF = ('row__id', 'row__name', 'period', 'value', 'row__row_type__name', 'row__row_group1__name',
               'row__row_group2__name', 'row__row_group3__name', 'data_type__name')

    def __init__(self):
        self.data = None

    def report_handler(self, kwargs):
        """Get DataFrame object from Report table."""
        report = Report.objects.filter(
            indicator=kwargs['indicator'], year=kwargs['year'], row_code__isnull=False
            ).select_related(*self.REPORT_RF).values(*self.REPORT_VF)
        return read_frame(report)

    def data_handler(self, kwargs, subquery):
        """Get DataFrame object from Data table."""
        data = Data.objects.filter(
            row__in=subquery['row'], org__in=subquery['branch'], period__year=kwargs['year'],
            data_type__name__in=subquery['forecast']
            ).select_related(*self.DATA_RF).values(*self.DATA_VF)
        return read_frame(data)

    def run_data_manager(self, kwargs, subquery):
        """Merge Report and Data DataFrame objects."""
        if self.data is None:
            report_df = self.report_handler(kwargs)
            data_df = self.data_handler(kwargs, subquery)
            self.data = data_df.merge(report_df, how='left', left_on='row__id', right_on='row_code') \
                .sort_values(by=['row_position', 'period'], ascending=True)


class BaseRowManager:
    DATA_TYPE = ('Actual', 'Budget')
    POSITION = ('numerator', 'denominator')

    def __init__(self):
        self.context_block = {}
        self.indicator_block = {}
        self.implementation_block = {}

    def context_handler(self, df_block, kwargs, subquery):
        """Create main template table context."""
        if not df_block.empty:
            for row_id in subquery['row']:
                sub_context_block = {}
                for data_type in subquery['forecast']:
                    sub_data_manager = df_block[
                        (df_block['row__id'] == row_id) & (df_block['data_type__name'] == data_type)]
                    if not sub_data_manager.empty:
                        sub_context_block[data_type] = self.context_row_handler(sub_data_manager)
                self.forecast_handler(sub_context_block, kwargs)
                self.result_handler(sub_context_block, kwargs, subquery)
                self.context_block[row_id] = sub_context_block

    @staticmethod
    def context_row_handler(sub_data_manager):
        """
        Convert pandas.DataFrame() block to dict().
        Return dict();
        """
        context_row = {}
        if not sub_data_manager.empty:
            for column in sub_data_manager.columns:
                if column == 'value':
                    context_row[column] = Series(sub_data_manager.groupby('period').sum()[column])
                else:
                    context_row[column] = sub_data_manager.iloc[0][column]
        return context_row

    def forecast_handler(self, sub_data_manager, kwargs):
        """
        Convert Actual block unused values to 0.
        Convert Forecast block unused values to 0.
        Merge Actual and Forecast block values.

        As result we get forecast sub_data_manager['Actual']['value'] block
        """
        if sub_data_manager:
            sub_data_manager['Actual']['value'].loc[sub_data_manager['Actual']['value'].index > kwargs['period']] = 0
            forecast_block = self.sub_forecast_handler(sub_data_manager, kwargs)
            forecast_block.loc[forecast_block.index <= kwargs['period']] = 0
            sub_data_manager['Actual']['value'] += forecast_block

    @staticmethod
    def sub_forecast_handler(sub_data_manager, kwargs):
        """
        Select forecast value block by condition.
        Return pandas.Series()
        """
        if kwargs['forecast'] == 1:
            return deepcopy(sub_data_manager['Budget']['value'])
        elif kwargs['forecast'] == 2:
            return deepcopy(sub_data_manager['RF1']['value'])
        elif kwargs['forecast'] == 3:
            return deepcopy(sub_data_manager['RF2']['value'])
        else:
            index = sub_data_manager['Actual']['value'].index
            return Series([0 for i in range(len(index))], index=index)

    def result_handler(self, *args, **kwargs):
        """
        Method for monthly or cumulative values representation.
        Override for current indicator.
        """
        pass

    def sub_result_handler(self, *args, **kwargs):
        """
        Supporting method for result handler.
        Override for current indicator.
        """
        pass

    def indicator_handler(self, *args, **kwargs):
        """Calculate indicator row values."""
        pass

    def sub_indicator_handler(self, *args, **kwargs):
        """Sub method for indicator values calculation."""
        pass

    def implementation_handler(self):
        """
        Calculate implementation row values.
        indicator['Actual'] / indicator['Budget']
        """
        if self.indicator_block:
            try:
                self.implementation_block = self.indicator_block['Actual']['value'] /\
                    self.indicator_block['Budget']['value']
            except (ZeroDivisionError, KeyError, TypeError):
                self.implementation_block = Series([0 for i in range(12)])

    def run_row_manager(self, *args, **kwargs):
        pass


class BaseController:
    def __init__(self, kwargs, managers):
        self.kwargs = kwargs
        self.managers = managers
        self.query_manager = None
        self.data_manager = None
        self.row_manager = None

    def create_subquery(self):
        if self.query_manager is None:
            self.query_manager = self.managers['query_manager']()
            self.query_manager.run_query_manager(self.kwargs)

    def create_data(self):
        if self.data_manager is None:
            self.data_manager = self.managers['data_manager']()
            self.data_manager.run_data_manager(self.kwargs, self.query_manager.query)

    def create_row(self):
        if self.row_manager is None:
            self.row_manager = self.managers['row_manager']()
            self.row_manager.run_row_manager(self.data_manager.data, self.kwargs, self.query_manager.query)

    def run_controller(self):
        self.create_subquery()
        self.create_data()
        self.create_row()