from django.shortcuts import render
from django.http import HttpResponseForbidden

from .calc_dashboard import DashController, managers, get_indicator_list
from main.models import Account, CurrentPeriod


def dash(request, id):
    """View information for current user or staff users."""
    if id == request.user.id or request.user.is_staff:
        # get current period
        current_period = CurrentPeriod.objects.first()
        # get indicator list for current user
        indicator_list = get_indicator_list(id, current_period.year)
        kwargs_list = []
        for indicator in indicator_list:
            kwargs = {
                'indicator': indicator,
                'year': current_period.year,
                'period': current_period.period,
                'user': id
                }
            kwargs_list.append(kwargs)
        context = {
            'current_user': Account.objects.get(id=id),
            'current_period': current_period.period,
            'dash_data': {}
            }
        # Rub dashboard calculator controller for each indicator in indicator list
        for kwargs in kwargs_list:
            dash_data = DashController(kwargs, managers)
            dash_data.run_controller()
            context['dash_data'][kwargs['indicator']] = {
                'kwargs': kwargs,
                'info': dash_data.query_manager.query['indicator'],
                'dash': dash_data.row_manager.dash_value,
                'scale': dash_data.scale_manager.scale,
                }
        return render(request, 'dashboard/dashboard_page.html', context)
    return HttpResponseForbidden('У вас нет доступа к этой странице')