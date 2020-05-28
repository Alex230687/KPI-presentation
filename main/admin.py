from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.sessions.models import Session
from .models import Account


class AccountFilter(SimpleListFilter):
    title = 'Катергория пользователей'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('manager', 'Менеджер'),
            ('director', 'Директор'),
            ('head', 'Руководитель'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'manager':
            return queryset.filter(is_manager=True, is_staff=False)
        elif self.value() == 'director':
            return queryset.filter(is_manager=False, is_staff=True)
        elif self.value() == 'head':
            return queryset.filter(is_manager=True, is_staff=True)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_manager', 'last_login', 'password')
    list_filter = (AccountFilter,)
    list_display_links = ('email',)
    list_editable = ('password', 'is_staff', 'is_active', 'is_manager')


admin.site.register(Account, AccountAdmin)


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, session):
        ses_dict = session.get_decoded()
        user_id = ses_dict['_auth_user_id']
        user = Account.objects.get(id=user_id)
        return user.email
    list_display = ['session_key', 'expire_date', '_session_data']


admin.site.register(Session, SessionAdmin)