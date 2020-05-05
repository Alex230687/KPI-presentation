from django.urls import path
from .views import dash


app_name = 'dashboard'
urlpatterns = [
    path('<int:id>/', dash, name='dash'),
]