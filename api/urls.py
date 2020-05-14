from django.urls import path
from .views import IndicatorLongDetailView


app_name = 'api'
urlpatterns = [
    path('indicator/<int:id>-<int:year>/', IndicatorLongDetailView.as_view()),
]
