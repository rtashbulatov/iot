import random
import time

import numpy as np
import requests

SERVER_ADDRESS = 'localhost'
SERVER_PORT = '8000'
SENSOR_ID = f'iot-sensor-moisture-{random.randint(0, 1000)}'


def get_last_watering_state():
    r = requests.get(url=f'http://{SERVER_ADDRESS}:{SERVER_PORT}/api/watering-state/')
    return r.json()['state']


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
        value = get_moisture_measure()

        if value is not None:
            data = {
                'sensor_id': SENSOR_ID,
                'type': 'moisture',
                'value': value
            }
            requests.post(f'http://{SERVER_ADDRESS}:{SERVER_PORT}/api/sensor-reading/', json=data, headers={'x-api-key': 'sensor'})
        else:
            print('Не удалось считать данные с датчика.')
        time.sleep(1)
except KeyboardInterrupt:
    print("Завершение работы...")
