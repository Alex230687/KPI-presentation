from copy import deepcopy
from pandas import Series
from django_pandas.io import read_frame
from main.models import Data, Row
from .calc_basic import BaseQueryManager, BaseDataManager, BaseController
from .calc_value_indicator import ValueRowManager
from .forms import BaseForm


class VariableQueryManager(BaseQueryManager):
    REVENUE = [10, 20, 30, 40, 50]

    def __init__(self):
        super().__init__()
        self.query.update(dict.fromkeys(['fixed', 'variable', 'revenue']))
        self.additional_chain = [self.fixed_query, self.variable_query, self.revenue_query]

    def fixed_query(self):
        if self.query['fixed'] is None and self.query['row']:
            self.query['fixed'] = Row.objects.filter(id__in=self.query['row'], row_type__name='fixed') \
                .values_list('id', flat=True)

    def variable_query(self):
        if self.query['variable'] is None and self.query['row']:
            self.query['variable'] = Row.objects.filter(id__in=self.query['row'], row_type__name='variable') \
                .values_list('id', flat=True)

    def revenue_query(self):
        if self.query['revenue'] is None:
            self.query['revenue'] = Row.objects.filter(id__in=self.REVENUE).values_list('id', flat=True)

    def run_query_manager(self, kwargs):
        for method in self.manager_chain:
            method(kwargs)
        for additional_method in self.additional_chain:
            additional_method()


class VariableDataManager(BaseDataManager):
    def __init__(self):
        super().__init__()
        self.revenue_data = None

    def revenue_handler(self, kwargs, subquery):
        revenue = Data.objects.filter(
            row__in=subquery['revenue'], org__in=subquery['branch'], period__year=kwargs['year'],
            data_type__name__in=subquery['forecast']
            ).select_related(*self.DATA_RF).values(*self.DATA_VF)
        self.revenue_data = read_frame(revenue)


class VariableRowManager(ValueRowManager):
    def __init__(self):
        super().__init__()
        self.revenue_context = {}
        self.sub_indicator_block = {}

    def revenue_row_handler(self, revenue_block, kwargs, subquery):
        if not revenue_block.empty:
            sub_revenue_context = {}
            for data_type in subquery['forecast']:
                sub_revenue_block = revenue_block[revenue_block['data_type__name'] == data_type]
                if not sub_revenue_block.empty:
                    sub_revenue_context[data_type] = self.context_row_handler(sub_revenue_block)
            self.forecast_handler(sub_revenue_context, kwargs)
            self.result_handler(sub_revenue_context, kwargs, subquery)
            self.revenue_context['revenue'] = sub_revenue_context

    def revenue_implementation_handler(self):
        if self.revenue_context:
            try:
                self.revenue_context['implementation'] = self.revenue_context['revenue']['Actual']['value'] /\
                    self.revenue_context['revenue']['Budget']['value']
            except (ZeroDivisionError, KeyError, TypeError):
                self.revenue_context['implementation'] = Series([0 for i in range(12)])

    def variable_handler(self):
        if self.context_block and self.revenue_context:
            for sub_context in self.context_block.keys():
                for data_type in self.context_block[sub_context].keys():
                    if self.context_block[sub_context][data_type]['row__row_type__name'] == 'variable' \
                            and data_type == 'Budget':
                        adjustment = deepcopy(self.revenue_context['implementation'])
                        adjustment.loc[adjustment == 0] = 1
                        self.context_block[sub_context][data_type]['value'] =\
                            self.context_block[sub_context][data_type]['value'] *\
                            (1 + (adjustment - 1))

    def sub_indicator_handler(self, df_block, kwargs, subquery):
        if not df_block.empty:
            for row_type in ('fixed', 'variable'):
                sub_indicator_context = {}
                for data_type in self.DATA_TYPE:
                    sub_df_block = df_block[
                        (df_block['row__row_type__name'] == row_type) & (df_block['data_type__name'] == data_type)]
                    if not sub_df_block.empty:
                        sub_indicator_context[data_type] = self.context_row_handler(sub_df_block)
                self.forecast_handler(sub_indicator_context, kwargs)
                self.result_handler(sub_indicator_context, kwargs, subquery)
                self.sub_indicator_block[row_type] = sub_indicator_context

    def indicator_handler(self, *args, **kwargs):
        if self.revenue_context and self.sub_indicator_block:
            self.indicator_block['Actual'] = {'value': None}
            self.indicator_block['Actual']['value'] = self.sub_indicator_block['fixed']['Actual']['value'] +\
                self.sub_indicator_block['variable']['Actual']['value']
            self.indicator_block['Budget'] = {'value': None}
            adjustment = deepcopy(self.revenue_context['implementation'])
            adjustment.loc[adjustment == 0] = 1
            self.indicator_block['Budget']['value'] = self.sub_indicator_block['fixed']['Budget']['value'] +\
                self.sub_indicator_block['variable']['Budget']['value'] * (1 + (adjustment - 1))

    def run_row_manager(self, df_block, kwargs, subquery, revenue_block=None):
        self.revenue_row_handler(revenue_block, kwargs, subquery)
        self.revenue_implementation_handler()
        self.context_handler(df_block, kwargs, subquery)
        self.variable_handler()
        self.sub_indicator_handler(df_block, kwargs, subquery)
        self.indicator_handler()
        self.implementation_handler()


class VariableController(BaseController):
    def create_data(self):
        if self.data_manager is None:
            self.data_manager = self.managers['data_manager']()
            self.data_manager.run_data_manager(self.kwargs, self.query_manager.query)
            self.data_manager.revenue_handler(self.kwargs, self.query_manager.query)

    def create_row(self):
        if self.row_manager is None:
            self.row_manager = self.managers['row_manager']()
            self.row_manager.run_row_manager(self.data_manager.data, self.kwargs, self.query_manager.query,
                                             self.data_manager.revenue_data)


variable_view_block = {
    'controller': VariableController,
    'managers': {
        'query_manager': VariableQueryManager,
        'data_manager': VariableDataManager,
        'row_manager': VariableRowManager,
    },
    'form': BaseForm,
}