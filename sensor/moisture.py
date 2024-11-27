import json
import time
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import random
import numpy as np


MQTT_BROKER = 'localhost'
MQTT_TOPIC = 'iot/moisture'
MQTT_PORT = 1883
MQTT_CLIENT_ID = f'iot-sensor-moisture-{random.randint(0, 1000)}'


def get_last_watering_state():
    msg = subscribe.simple('iot/watering', hostname=MQTT_BROKER, port=MQTT_PORT)
    data = json.loads(msg.payload.decode("utf-8"))
    return data['state']


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, MQTT_CLIENT_ID)
client.connect(MQTT_BROKER, MQTT_PORT, 60)


current_moisture = random.uniform(5, 30)


def get_moisture_measure():
    global current_moisture
    state = get_last_watering_state()
    if state == 'on':
        external_influence = max(0, np.random.normal(1, 1))
    else:
        external_influence = -random.uniform(1, 3)
    current_moisture = min(max(current_moisture + external_influence, 5), 50)
    print(state, current_moisture)
    return current_moisture


try:
    while True:
        moisture = get_moisture_measure()
        client.loop()

        if moisture is not None:
            data = {
                'moisture': moisture
            }
            client.publish(MQTT_TOPIC, json.dumps(data), retain=True)
        else:
            print('Не удалось считать данные с датчика.')
        time.sleep(1)
except KeyboardInterrupt:
    print("Завершение работы...")
finally:
    client.disconnect()