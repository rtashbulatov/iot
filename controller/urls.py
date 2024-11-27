from django.urls import path
from .views import humidity_chart, illuminance_chart

urlpatterns = [
    path('humidity-chart/', humidity_chart, name='humidity_chart'),
    path('illuminance-chart/', illuminance_chart, name='illuminance_chart'),
]