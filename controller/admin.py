from django.contrib import admin
from .models import HoodActuatorConfig, LampActuatorConfig

# Register your models here.
admin.site.register(HoodActuatorConfig)
admin.site.register(LampActuatorConfig)
