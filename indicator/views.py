import datetime

from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.core.cache import cache
# from django.views.decorators.cache import cache_page
# from django.views.decorators.vary import vary_on_headers

from .calc_percent_indicator import percent_view_block
from .calc_turnover_indicator import turnover_view_block
from .calc_value_indicator import value_view_block
from .calc_variable_indicator import variable_view_block
from .tasks import write_form_query_log
from main.models import  CurrentPeriod
from dashboard.calc_dashboard import get_indicator_list


# create controllers dict
calc_block = {
    'percent': percent_view_block,
    'turnover': turnover_view_block,
    'value': value_view_block,
    'variable': variable_view_block,
}


def get_or_set_cached_object(kwargs, Controller, managers):
    """
    Function return controller object to create context block for template.
    1. Generate cache_key for current form-request data
        Example: Ebitda Moscow 2019 YTD No-forecast -> 'i-1-b-1-y-2019-t-1-f-0'
    2. If key in Memcached > get object > else create new controller
    """
    cache_key = 'i-%(indicator)s-b-%(branch)s-y-%(year)s-t-%(result)s-f-%(forecast)s' % (kwargs)
    if cache.has_key(cache_key):
        controller = cache.get(cache_key)
    else:
        controller = Controller(kwargs, managers)
        controller.run_controller()
        cache.set(cache_key, controller)
    return controller


def indicator(request, slug, id):
    """
    View indicator table.
    Choose indicator controller by <slug>
    """
    current_period = CurrentPeriod.objects.all().first()
    indicator_list = get_indicator_list(request.user.id, current_period.year)
    if id in indicator_list or request.user.is_staff:
        # set from, controller and managers for current indicator
        Form = calc_block[slug]['form']
        Controller = calc_block[slug]['controller']
        managers = calc_block[slug]['managers']
        if request.method == 'POST':
            form = Form(request.POST, indicator=id, year=current_period.year)
            if form.is_valid():
                # FORM QUERY LOG #############################################
                log_data = {
                    'user_id': request.user.id,
                    'log_time': datetime.datetime.utcnow(),
                    'form_year': int(form.cleaned_data['year']),
                    'form_branch': form.cleaned_data['branch'].id,
                    'form_forecast': int(form.cleaned_data['forecast']),
                    'form_totals': int(form.cleaned_data['ytd']),
                }
                write_form_query_log.delay(log_data)
                ##############################################################

                kwargs = {
                    'indicator': id,
                    'branch': form.cleaned_data['branch'].id,
                    'year': int(form.cleaned_data['year']),
                    'result': int(form.cleaned_data['ytd']),
                    'forecast': int(form.cleaned_data['forecast']),
                    'period': current_period.period
                }

                # GET CACHED OBJECT OR CREATE NEW CACHED OBJECT
                controller = get_or_set_cached_object(kwargs, Controller, managers)
                ################################################

                context = {
                    'form': form,
                    'kwargs': kwargs,
                    'table': controller.row_manager.context_block,
                    'indicator': controller.row_manager.indicator_block,
                    'implementation': controller.row_manager.implementation_block,
                    'info': controller.query_manager.query['indicator'],
                }
                return render(request, 'indicator/indicator_page.html', context)
        else:
            form = Form(indicator=id, year=current_period.year)
        context = {'form': form}
        return render(request, 'indicator/indicator_page.html', context)
    else:
        return HttpResponseForbidden("У вас нет доступа к этой странице!")
