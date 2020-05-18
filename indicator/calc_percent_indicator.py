from pandas import Series

from .calc_basic import BaseDataManager, BaseController, BaseQueryManager
from .calc_value_indicator import ValueRowManager
from .forms import BaseForm


class PercentQueryManager(BaseQueryManager):
    pass


class PercentDataManager(BaseDataManager):
    pass


class PercentRowManager(ValueRowManager):
    """Manager create necessary table information for indicator."""
    def indicator_handler(self, df_block, kwargs, subquery):
        """Calculate indicator row values."""
        position_block = {}
        for position in self.POSITION:
            sub_position_block = {}
            for data_type in subquery['forecast']:
                df_group = self.context_row_handler(
                    df_block[(df_block['data_type__name'] == data_type) & (df_block[position] == 1)])
                sub_position_block[data_type] = df_group
            self.forecast_handler(sub_position_block, kwargs)
            self.result_handler(sub_position_block, kwargs, subquery)
            position_block[position] = sub_position_block
        self.sub_indicator_handler(position_block)

    def sub_indicator_handler(self, position_block):
        """Sub method for indicator values calculation."""
        for data_type in self.DATA_TYPE:
            self.indicator_block[data_type] = {'value': None}
            try:
                self.indicator_block[data_type]['value'] = position_block['numerator'][data_type]['value'] /\
                    position_block['denominator'][data_type]['value']
            except (ZeroDivisionError, KeyError, TypeError):
                self.indicator_block[data_type] = Series([0 for i in range(12)])


class PercentController(BaseController):
    pass


# controller block
percent_view_block = {
    'controller': PercentController,
    'managers': {
        'query_manager': PercentQueryManager,
        'data_manager': PercentDataManager,
        'row_manager': PercentRowManager,
    },
    'form': BaseForm,
}
