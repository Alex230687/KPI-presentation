import datetime
from pandas import Series
from django_pandas.io import read_frame
from main.models import Report, Data
from .calc_basic import BaseQueryManager, BaseDataManager, BaseController
from .calc_percent_indicator import PercentRowManager
from .forms import TurnoverForm


class TurnoverQueryManager(BaseQueryManager):
    def __init__(self):
        super().__init__()
        self.query.update(dict.fromkeys(['numerator', 'denominator']))
        self.manager_chain.extend([self.numerator_query, self.denominator_query])

    def numerator_query(self, kwargs):
        if self.query['numerator'] is None:
            self.query['numerator'] = Report.objects.filter(
                indicator=kwargs['indicator'], year=kwargs['year'], numerator__isnull=False
                ).values_list('row_code', flat=True)

    def denominator_query(self, kwargs):
        if self.query['denominator'] is None:
            self.query['denominator'] = Report.objects.filter(
                indicator=kwargs['indicator'], year=kwargs['year'], denominator__isnull=False
                ).values_list('row_code', flat=True)


class TurnoverDataManager(BaseDataManager):
    """For turnover block select 24-month period."""
    def report_handler(self, kwargs):
        """Report block overriding."""
        report = Report.objects.filter(
            indicator=kwargs['indicator'], year__in=[kwargs['year'], kwargs['year']-1], row_code__isnull=False
        ).select_related(*self.REPORT_RF).values(*self.REPORT_VF)
        return read_frame(report)

    def data_handler(self, kwargs, subquery):
        """Data block overriding."""
        data = Data.objects.filter(
            row__in=subquery['row'], org__in=subquery['branch'], period__year__in=[kwargs['year'], kwargs['year']-1],
            data_type__name__in=subquery['forecast']
        ).select_related(*self.DATA_RF).values(*self.DATA_VF)
        return read_frame(data)


class TurnoverRowManager(PercentRowManager):
    def __init__(self):
        super().__init__()
        self.sub_implementation_block = {}

    def result_handler(self, sub_context_block, kwargs, subquery):
        for data_type in subquery['forecast']:
            if kwargs['result'] == 1:
                sub_context_block[data_type]['value'] = self.sub_result_handler(
                    sub_context_block[data_type]['value'], kwargs, 'average')
            else:
                sub_context_block[data_type]['value'] = self.sub_result_handler(
                    sub_context_block[data_type]['value'], kwargs, 'current')

    def sub_result_handler(self, sub_value_block, kwargs, selection):
        """
        Create pandas.Series() to convert 24-month block to 12-month.
        For BALANCE rows use current month value.
        For PNL rows use 12-month-slice value.
        """
        index = [datetime.date(kwargs['year'], i, 1) for i in range(1, 13)]
        sub_block = Series([0 for i in range(len(index))], index=index)
        for date in index:
            if selection == 'current':
                sub_block.loc[sub_block.index == date] = sub_value_block.loc[sub_value_block.index == date]
            elif selection == 'average':
                sub_block.loc[sub_block.index == date] = sub_value_block.loc[
                    (sub_value_block.index <= date) & (sub_value_block.index >= self.start_date(date))
                    ].mean()
        if kwargs['forecast'] == 0:
            sub_block.loc[sub_block.index > kwargs['period']] = 0
        return sub_block

    @staticmethod
    def start_date(date):
        """Create datetime.date() object for 12-month-period slice."""
        if date.month < 12:
            return datetime.date(date.year - 1, date.month + 1, 1)
        else:
            return datetime.date(date.year, 1, 1)

    def run_row_manager(self, df_block, kwargs, subquery):
        self.context_handler(df_block, kwargs, subquery)
        self.indicator_handler(df_block, kwargs, subquery)
        self.implementation_handler()


class TurnoverController(BaseController):
    pass


turnover_view_block = {
    'controller': TurnoverController,
    'managers': {
        'query_manager': TurnoverQueryManager,
        'data_manager': TurnoverDataManager,
        'row_manager': TurnoverRowManager,
    },
    'form': TurnoverForm,
}