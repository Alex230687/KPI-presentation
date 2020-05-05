from .models import Scale, Indicator


def get_indicator_info(user_id, year):
    """
    Function create indicator info block for navigation bar.
    1) create subquery of unique indicator_id list from Scale table by user_id and current year;
    2) create queryset of indicator information by subquery;
    """
    subquery = Scale.objects.filter(account=user_id, year=year).values_list('indicator', flat=True).distinct()
    # info = Indicator.objects.filter(id__in=subquery).select_related('indicator_effect', 'indicator_group').\
    #     values('id', 'name', 'indicator_effect__name', 'indicator_group__name')
    info = Indicator.objects.filter(id__in=subquery).select_related('indicator_effect', 'indicator_group')
    return info
