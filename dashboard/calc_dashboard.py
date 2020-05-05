import datetime
from django.db.models import Sum
from main.models import Scale, Report, Data, Target, Indicator


def get_indicator_list(account, year):
    return Scale.objects.filter(account=account, year=year).values_list('indicator', flat=True).distinct()


class DashQueryManager:
    def __init__(self):
        self.query = dict.fromkeys(['row', 'branch', 'target', 'indicator', 'numerator', 'denominator'])

    def row_query(self, kwargs):
        if self.query['row'] is None:
            self.query['row'] = Report.objects.filter(
                indicator=kwargs['indicator'], year=kwargs['year'], row_code__isnull=False
                ).values_list('row_code', flat=True)

    def branch_query(self, kwargs):
        if self.query['branch'] is None:
            self.query['branch'] = Report.objects.filter(
                indicator=kwargs['indicator'], year=kwargs['year'], org_code__isnull=False
                ).values_list('org_code', flat=True)

    def target_query(self, kwargs):
        if self.query['target'] is None:
            self.query['target'] = Target.objects.filter(indicator=kwargs['indicator'], year=kwargs['year']) \
                .values_list('target', flat=True)[0]

    def indicator_query(self, kwargs):
        RF = ('indicator_effect', 'indicator_group')
        VF = ('id', 'name', 'slag', 'indicator_effect__name', 'indicator_group__name')
        if self.query['indicator'] is None:
            self.query['indicator'] = Indicator.objects.filter(id=kwargs['indicator']) \
                .select_related(*RF).values(*VF)[0]

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

    def run_query_manager(self, kwargs):
        self.row_query(kwargs)
        self.branch_query(kwargs)
        self.target_query(kwargs)
        self.indicator_query(kwargs)
        self.numerator_query(kwargs)
        self.denominator_query(kwargs)


class DashRowManager:
    def __init__(self):
        self.dash_value = dict.fromkeys(['Actual', 'Budget', 'Implementation'])
        self.revenue_block = dict.fromkeys(['Actual', 'Budget', 'Implementation'])

    def calculate_implementation(self):
        if self.dash_value['Implementation'] is None:
            try:
                self.dash_value['Implementation'] = self.dash_value['Actual'] / self.dash_value['Budget']
            except (ZeroDivisionError, KeyError, TypeError):
                self.dash_value['Implementation'] = 0

    def get_amount_data(self, kwargs, subquery):
        for data_type in ('Actual', 'Budget'):
            self.dash_value[data_type] = Data.objects.filter(
                row__in=subquery['row'], org__in=subquery['branch'], data_type__name=data_type,
                period__year=kwargs['year'], period__lte=kwargs['period']).aggregate(sm=Sum('value'))['sm']

    def get_percent_data(self, kwargs, subquery):
        for data_type in ('Actual', 'Budget'):
            if 'numerator' in subquery.keys() and 'denominator' in subquery.keys():
                if subquery['numerator'] and subquery['denominator']:
                    sub_dict = {}
                    for position in ('numerator', 'denominator'):
                        sub_dict[position] = abs(Data.objects.filter(
                            row__in=subquery[position], org__in=subquery['branch'], data_type__name=data_type,
                            period__year=kwargs['year'], period__lte=kwargs['period']).aggregate(sm=Sum('value'))['sm'])
                    try:
                        self.dash_value[data_type] = sub_dict['numerator'] / sub_dict['denominator']
                    except (ZeroDivisionError, KeyError, TypeError):
                        self.dash_value[data_type] = 0

    def get_variable_data(self, kwargs, subquery):
        for data_type in ('Actual', 'Budget'):
            sub_data_dict = {}
            for row_type in ('fixed', 'variable'):
                sub_data_dict[row_type] = abs(Data.objects.filter(
                    row__in=subquery['row'], row__row_type__name=row_type, org__in=subquery['branch'],
                    data_type__name=data_type, period__year=kwargs['year'], period__lte=kwargs['period']
                ).aggregate(sm=Sum('value'))['sm'])

            try:
                self.dash_value[data_type] = sub_data_dict['fixed'] + (
                        sub_data_dict['variable'] * (1 + (self.revenue_block['Implementation']) - 1)
                        )
            except (ZeroDivisionError, KeyError, TypeError):
                self.dash_value[data_type] = sub_data_dict['fixed'] + sub_data_dict['variable']

    def get_turnover_data(self, kwargs, subquery):
        for data_type in ('Actual', 'Budget'):
            if subquery['target'] and data_type == 'Budget':
                self.dash_value['Budget'] = subquery['target']
            else:
                if 'numerator' in subquery.keys() and 'denominator' in subquery.keys():
                    if subquery['numerator'] and subquery['denominator']:
                        sub_dict = {}
                        for position in ('numerator', 'denominator'):
                            sub_dict[position] = abs(Data.objects.filter(
                                row__in=subquery[position], org__in=subquery['branch'], data_type__name=data_type,
                                period__gte=self.get_month_range(kwargs['period']), period__lte=kwargs['period']
                                ).aggregate(sm=Sum('value'))['sm'] / 12)
                        try:
                            self.dash_value[data_type] = sub_dict['numerator'] / sub_dict['denominator']
                        except (ZeroDivisionError, TypeError, KeyError):
                            self.dash_value[data_type] = 0

    @staticmethod
    def get_month_range(period):
        if period.month < 12:
            return datetime.date(period.year-1, period.month+1, period.day)
        else:
            return datetime.date(period.year, 1, period.day)

    def get_revenue_block(self, kwargs, subquery):
        for data_type in ('Actual', 'Budget'):
            self.revenue_block[data_type] = Data.objects.filter(
                org__in=subquery['branch'], data_type__name=data_type, period__year=kwargs['year'],
                period__lte=kwargs['period'], row__row_group3=10
                ).aggregate(sm=Sum('value'))['sm']
        try:
            self.revenue_block['Implementation'] = self.revenue_block['Actual'] / self.revenue_block['Budget']
        except (ZeroDivisionError, KeyError, TypeError):
            self.revenue_block['Implementation'] = 0

    def run_row_manager(self, kwargs, subquery):
        if subquery['indicator']['indicator_group__name'] == 'value':
            self.get_amount_data(kwargs, subquery)
        elif subquery['indicator']['indicator_group__name'] == 'percent':
            self.get_percent_data(kwargs, subquery)
        elif subquery['indicator']['indicator_group__name'] == 'turnover':
            self.get_turnover_data(kwargs, subquery)
        elif subquery['indicator']['indicator_group__name'] == 'variable':
            self.get_revenue_block(kwargs, subquery)
            self.get_variable_data(kwargs, subquery)
        else:
            pass
        self.calculate_implementation()


class DashScaleManager:
    SCALE_VAL_FIELDS = ('row_position', 'percent_min', 'percent_max', 'bonus_min', 'bonus_max', 'bonus_share')

    def __init__(self):
        self.scale = None

    def create_scale_block(self, kwargs):
        if self.scale is None:
            self.scale = Scale.objects.filter(
                account=kwargs['user'], year=kwargs['year'], indicator=kwargs['indicator']
                ).order_by('row_position').values(*self.SCALE_VAL_FIELDS)


managers = {
    'query_manager': DashQueryManager,
    'row_manager': DashRowManager,
    'scale_manager': DashScaleManager,
    }


class DashController:
    def __init__(self, kwargs, managers):
        self.kwargs = kwargs
        self.managers = managers
        self.query_manager = None
        self.row_manager = None
        self.scale_manager = None

    def create_subquery(self):
        if self.query_manager is None:
            self.query_manager = self.managers['query_manager']()
            self.query_manager.run_query_manager(self.kwargs)

    def create_row(self):
        if self.row_manager is None:
            self.row_manager = self.managers['row_manager']()
            self.row_manager.run_row_manager(self.kwargs, self.query_manager.query)

    def create_scale(self):
        if self.scale_manager is None:
            self.scale_manager = self.managers['scale_manager']()
            self.scale_manager.create_scale_block(self.kwargs)

    def run_controller(self):
        self.create_subquery()
        self.create_row()
        self.create_scale()
