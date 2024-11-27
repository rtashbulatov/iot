import json
import paho.mqtt.client as mqtt
from django.conf import settings


from datetime import datetime


def send_mqtt_hood_message(mqtt_client, speed, retain=True):
    data = {
        'speed': speed
    }
    mqtt_client.publish('iot/hood', json.dumps(data), retain=retain)


def send_mqtt_lamp_message(mqtt_client, state, retain=True):
    data = {
        'state': state
    }
    mqtt_client.publish('iot/lamp', json.dumps(data), retain=retain)


def on_connect_humidity(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe('iot/humidity')
        send_mqtt_hood_message(mqtt_client, 0, True)
    else:
        print('Bad connection. Code:', rc)


def on_message_humidity(mqtt_client, userdata, msg):
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


def on_connect_illuminance(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe('iot/illuminance')
        send_mqtt_lamp_message(mqtt_client, 'off', True)
    else:
        print('Bad connection. Code:', rc)


def on_message_illuminance(mqtt_client, userdata, msg):
    from .models import SensorReading, LampActuatorConfig
    try:
        print(f'Received message on topic!: {msg.topic} with payload: {msg.payload}')
        data = json.loads(msg.payload.decode('utf-8'))
        reading = SensorReading(reading_type='illuminance', reading_value=data['illuminance'], timestamp=datetime.now())
        reading.save()

        config = LampActuatorConfig.objects.all()[0]
        if data['illuminance'] <= config.min_value:
            send_mqtt_hood_message(mqtt_client, 'on')
        else:
            send_mqtt_hood_message(mqtt_client, 'off')
    except Exception as e:
        print("Decode error")



humidity_client = mqtt.Client()
humidity_client.on_connect = on_connect_humidity
humidity_client.on_message = on_message_humidity
humidity_client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
humidity_client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE
)

illuminance_client = mqtt.Client()
humidity_client.on_connect = on_connect_illuminance
humidity_client.on_message = on_message_illuminance
humidity_client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
humidity_client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE
)

