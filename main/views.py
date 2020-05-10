from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def main(request):
    return render(request, 'main/main_page.html')


class AccountLogin(LoginView):
    template_name = 'main/login_page.html'


class AccountLogout(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout_page.html'
# CELERY BLOCK TEST
