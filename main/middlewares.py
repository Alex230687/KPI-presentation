from django.contrib.auth.models import AnonymousUser
from .models import CurrentPeriod
from .utilities import get_indicator_info


def indicator_list_for_navbar(request):
    context = {}
    # if request.user.__class__ is not AnonymousUser:
    if request.user.is_authenticated:
        if request.user.is_manager:
            user_id = request.user.id
            period = CurrentPeriod.objects.first()
            indicator_info = get_indicator_info(user_id, period.year)
            context['current_period'] = period
            context['indicator_info'] = indicator_info
    return context
