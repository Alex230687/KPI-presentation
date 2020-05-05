from .calc_basic import BaseQueryManager, BaseDataManager, BaseRowManager, BaseController
from .forms import BaseForm


class ValueQueryManager(BaseQueryManager):
    pass


class ValueDataManager(BaseDataManager):
    pass


class ValueRowManager(BaseRowManager):
    def result_handler(self, sub_context_block, kwargs, subquery):
        for data_type in subquery['forecast']:
            if kwargs['result'] == 1:
                sub_context_block[data_type]['value'] = sub_context_block[data_type]['value'].cumsum()
                if kwargs['forecast'] == 0 and data_type == 'Actual':
                    sub_context_block[data_type]['value'].loc[
                        sub_context_block[data_type]['value'].index > kwargs['period']
                        ] = 0

    def indicator_handler(self, df_block, kwargs, subquery):
        if not df_block.empty:
            for data_type in subquery['forecast']:
                df_group = self.context_row_handler(df_block[df_block['data_type__name'] == data_type])
                self.indicator_block[data_type] = df_group
            self.forecast_handler(self.indicator_block, kwargs)
            self.result_handler(self.indicator_block, kwargs, subquery)

    def run_row_manager(self, df_block, kwargs, subquery):
        self.context_handler(df_block, kwargs, subquery)
        self.indicator_handler(df_block, kwargs, subquery)
        self.implementation_handler()


class ValueController(BaseController):
    pass


value_view_block = {
    'controller': ValueController,
    'managers': {
        'query_manager': ValueQueryManager,
        'data_manager': ValueDataManager,
        'row_manager': ValueRowManager,
    },
    'form': BaseForm,
}