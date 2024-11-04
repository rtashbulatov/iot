import json
import paho.mqtt.client as mqtt
from django.conf import settings


from datetime import datetime


def send_mqtt_hood_message(mqtt_client, speed, retain=True):
    data = {
        'speed': speed
    }
    mqtt_client.publish('iot/hood', json.dumps(data), retain=retain)


def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe('iot/humidity')
        send_mqtt_hood_message(mqtt_client, 0, True)
    else:
        print('Bad connection. Code:', rc)


def on_message(mqtt_client, userdata, msg):
    from .models import SensorReading, HoodActuatorConfig
    try:
        print(f'Received message on topic!: {msg.topic} with payload: {msg.payload}')
        data = json.loads(msg.payload.decode('utf-8'))
        reading = SensorReading(reading_type='humidity', reading_value=data['humidity'], timestamp=datetime.now())
        reading.save()

        config = HoodActuatorConfig.objects.all()[0]
        if data['humidity'] >= config.min_value:
            send_mqtt_hood_message(mqtt_client, config.hood_speed)
            print(f"{config.hood_speed}")
        else:
            send_mqtt_hood_message(mqtt_client, 0)
            print(0)
    except Exception as e:
        print("Decode error")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE
)
