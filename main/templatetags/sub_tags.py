from django.template.defaulttags import register


@register.filter
def item(dict_object, key):
    """Get key value from dict object."""
    return dict_object.get(key)


@register.filter
def percent(value, digit=None):
    """
    Format decimal number to percent format.
    If value is None or 'nan' returns empty string (DataFrame object sometime return 'nan').
    Arg digit set decimal length, but not more then 2.
    If digit == 0 return x% format.
    """
    pattern = '{:.%s%%}'
    if value and str(value) != 'nan':
        if digit is not None:
            if digit > 2:
                return (pattern % 2).format(value)
            else:
                return (pattern % digit).format(value)
        else:
            return (pattern % 0).format(value)
    return ""


@register.filter
def turnover(value):
    """
    Format value to x.xx format.
    Use for turnover indicator only!
    If value is None or 'nan' returns empty string (DataFrame object sometime return 'nan').
    """
    if value and str(value) != 'nan':
        return '{:.2}'.format(value)
    return ""


@register.filter
def index(list_object, position):
    """Get element from list object by position."""
    if list_object and isinstance(position, int) and position < len(list_object):
        return list_object[position]
    return ""

