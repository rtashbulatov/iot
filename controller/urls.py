from django.urls import path
from .views import humidity_chart, illuminance_chart, moisture_chart, temperature_chart

urlpatterns = [
    path('humidity-chart/', humidity_chart, name='humidity_chart'),
    path('illuminance-chart/', illuminance_chart, name='illuminance_chart'),
    path('moisture-chart/', moisture_chart, name='moisture_chart'),
    path('temperature-chart/', temperature_chart, name='temperature_chart'),
]