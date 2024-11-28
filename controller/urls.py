from django.urls import path
from .views import humidity_chart, illuminance_chart, moisture_chart, temperature_chart, add_sensor_reading, get_hood_speed, get_watering_state

urlpatterns = [
    path('humidity-chart/', humidity_chart, name='humidity_chart'),
    path('illuminance-chart/', illuminance_chart, name='illuminance_chart'),
    path('moisture-chart/', moisture_chart, name='moisture_chart'),
    path('temperature-chart/', temperature_chart, name='temperature_chart'),
    path('api/sensor-reading/', add_sensor_reading, name='add_sensor_reading'),
    path('api/hood-speed/', get_hood_speed, name='get_hood_speed'),
    path('api/watering-state/', get_watering_state, name='get_watering_state')
]