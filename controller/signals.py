from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import HoodActuatorConfig
from .mqtt import client, send_mqtt_hood_message


@receiver(pre_save, sender=HoodActuatorConfig)
def mymodel_pre_save(sender, instance, **kwargs):
    if instance.pk:
        send_mqtt_hood_message(client, instance.hood_speed)
