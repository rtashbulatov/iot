import json
import math
import time
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import random
import numpy as np


MQTT_BROKER = 'localhost'
MQTT_TOPIC = 'iot/illuminance'
MQTT_PORT = 1883
MQTT_CLIENT_ID = f'iot-sensor-illuminance-{random.randint(0, 1000)}'


def get_last_lamp_state():
    msg = subscribe.simple('iot/lamp', hostname=MQTT_BROKER, port=MQTT_PORT)
    data = json.loads(msg.payload.decode("utf-8"))
    return data['state']


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, MQTT_CLIENT_ID)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

i = 0
current_illuminance = 0
max_illuminance = 20000


def get_illuminance_measure():
    global current_illuminance, i
    i += 2
    current_illuminance = max(0.0, math.sin(i * 0.1) * max_illuminance)
    print(current_illuminance)
    return current_illuminance


try:
    while True:
        illuminance = get_illuminance_measure()
        client.loop()

        if illuminance is not None:
            data = {
                'illuminance': illuminance
            }
            client.publish(MQTT_TOPIC, json.dumps(data), retain=True)
        else:
            print('Не удалось считать данные с датчика.')
        time.sleep(1)
except KeyboardInterrupt:
    print("Завершение работы...")
finally:
    client.disconnect()