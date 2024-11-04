from django.urls import path
from .views import humidity_chart

urlpatterns = [
    path('humidity-chart/', humidity_chart, name='humidity_chart')
    # другие маршруты
]