from django.urls import path
from .views import main, AccountLogin, AccountLogout


app_name = 'main'
urlpatterns = [
    path('main/logout/', AccountLogout.as_view(), name='logout'),
    path('main/login/', AccountLogin.as_view(), name='login'),
    path('main/', main, name='main'),
]