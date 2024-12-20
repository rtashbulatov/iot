from django.db import models


class SensorReading(models.Model):
    reading_type = models.CharField(max_length=128, null=False, blank=False, db_index=True)
    reading_value = models.FloatField(null=False, blank=False)
    timestamp = models.DateTimeField(null=False, blank=False)


class HoodActuatorConfig(models.Model):
    min_value = models.FloatField(null=False, blank=False)
    hood_speed = models.IntegerField(null=False, blank=False)


class LampActuatorConfig(models.Model):
    min_value = models.FloatField(null=False, blank=False)


class WateringActuatorConfig(models.Model):
    min_value = models.FloatField(null=False, blank=False)
    max_value = models.FloatField(null=False, blank=False)


class TemperatureNotificationConfig(models.Model):
    threshold = models.FloatField(null=False, blank=False)
    is_excess = models.BooleanField(null=False, blank=False)
    text = models.TextField(null=False, blank=False)
