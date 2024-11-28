import random
import numpy as np
import requests


SERVER_ADDRESS = 'localhost'
SERVER_PORT = '8000'
SENSOR_ID = f'iot-sensor-humidity-{random.randint(0, 1000)}'


def get_last_hood_speed():
    r = requests.get(url=f'http://{SERVER_ADDRESS}:{SERVER_PORT}/api/hood-speed/')
    return r.json()['speed']


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
        value = get_humidity_measure()

        if value is not None:
            data = {
                'sensor_id': SENSOR_ID,
                'type': 'humidity',
                'value': value
            }
            requests.post(f'http://{SERVER_ADDRESS}:{SERVER_PORT}/api/sensor-reading/', json=data, headers={'x-api-key': 'sensor'})
        else:
            print('Не удалось считать данные с датчика.')
except KeyboardInterrupt:
    print("Завершение работы...")
