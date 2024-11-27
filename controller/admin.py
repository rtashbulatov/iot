from django.contrib import admin
from .models import HoodActuatorConfig, LampActuatorConfig, WateringActuatorConfig

# Register your models here.
admin.site.register(HoodActuatorConfig)
admin.site.register(LampActuatorConfig)
admin.site.register(WateringActuatorConfig)
