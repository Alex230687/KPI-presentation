from django.urls import path
from .views import main, AccountLogin, AccountLogout


app_name = 'main'
urlpatterns = [
    path('logout/', AccountLogout.as_view(), name='logout'),
    path('login/', AccountLogin.as_view(), name='login'),
    path('', main, name='main'),
]