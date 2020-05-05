from django.urls import path
from .views import indicator


app_name = 'indicator'
urlpatterns = [
    path('<str:slag>/<int:id>/', indicator, name='indicator'),
]