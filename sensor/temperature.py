import json
import math
import random
import time

import numpy as np
import paho.mqtt.client as mqtt

MQTT_BROKER = 'localhost'
MQTT_TOPIC = 'iot/temperature'
MQTT_PORT = 1883
MQTT_CLIENT_ID = f'iot-sensor-temperature-{random.randint(0, 1000)}'


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, MQTT_CLIENT_ID)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

i = 0
current_temperature = 20
max_temperature = 40


def get_illuminance_measure():
    global current_temperature, i
    i += 2
    current_temperature = math.sin(i * 0.1) * max_temperature
    print(current_temperature)
    return current_temperature


try:
    while True:
        temperature = get_illuminance_measure()
        client.loop()

        if temperature is not None:
            data = {
                'temperature': temperature
            }
            client.publish(MQTT_TOPIC, json.dumps(data), retain=True)
        else:
            print('Не удалось считать данные с датчика.')
        time.sleep(1)
except KeyboardInterrupt:
    print("Завершение работы...")
finally:
    client.disconnect()
