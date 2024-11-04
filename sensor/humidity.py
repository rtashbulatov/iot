import json
import time
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import random
import numpy as np


MQTT_BROKER = 'localhost'
MQTT_TOPIC = 'iot/humidity'
MQTT_PORT = 1883
MQTT_CLIENT_ID = f'iot-sensor-humidity-{random.randint(0, 1000)}'


def get_last_hood_speed():
    msg = subscribe.simple('iot/hood', hostname=MQTT_BROKER, port=MQTT_PORT)
    data = json.loads(msg.payload.decode("utf-8"))
    return data['speed']


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, MQTT_CLIENT_ID)
client.connect(MQTT_BROKER, MQTT_PORT, 60)


current_humidity = random.uniform(25, 75)


def get_humidity_measure():
    global current_humidity
    external_influence = np.random.normal(1, 1)
    hood_speed = get_last_hood_speed()
    hood_influence = -hood_speed
    current_humidity = min(max(current_humidity + external_influence + hood_influence, 25), 75)
    print(hood_speed, current_humidity)
    return current_humidity


try:
    while True:
        humidity = get_humidity_measure()
        client.loop()

        if humidity is not None:
            data = {
                'humidity': humidity
            }
            client.publish(MQTT_TOPIC, json.dumps(data), retain=True)
        else:
            print('Не удалось считать данные с датчика.')
        time.sleep(1)
except KeyboardInterrupt:
    print("Завершение работы...")
finally:
    client.disconnect()