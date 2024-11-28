from django.contrib import admin
from .models import HoodActuatorConfig, LampActuatorConfig, WateringActuatorConfig, TemperatureNotificationConfig

# Register your models here.
admin.site.register(HoodActuatorConfig)
admin.site.register(LampActuatorConfig)
admin.site.register(WateringActuatorConfig)
admin.site.register(TemperatureNotificationConfig)
