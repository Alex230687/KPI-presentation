from django import forms
from main.models import Report, Organization, CurrentPeriod


period_list = CurrentPeriod.objects.values_list('year', flat=True).distinct()


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        indicator = kwargs.pop('indicator')
        year = kwargs.pop('year')
        super().__init__(*args, **kwargs)

        subquery = Report.objects.filter(indicator__id=indicator, year=year, org_code__isnull=False) \
            .values_list('org_code', flat=True)
        self.fields['branch'] = forms.ModelChoiceField(
            queryset=Organization.objects.filter(id__in=[*subquery, 6]), label='Филиал'
        )

    year = forms.ChoiceField(choices=[(year, year) for year in period_list], label='Год')
    ytd = forms.ChoiceField(choices=[(0, 'Месяц'), (1, 'Накопительно')], label='Итоги')
    forecast = forms.ChoiceField(choices=[(0, 'Без прогноза'), (1, 'Бюджет'), (2, 'RF1'), (3, 'RF3')], label='Прогноз')


class TurnoverForm(BaseForm):
    ytd = forms.ChoiceField(choices=[(0, 'Месяц'), (1, 'Среднегодовые')], label='Итоги')