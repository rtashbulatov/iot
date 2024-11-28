import math
import random
import time

import requests

SERVER_ADDRESS = 'localhost'
SERVER_PORT = '8000'
SENSOR_ID = f'iot-sensor-illuminance-{random.randint(0, 1000)}'


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
        value = get_illuminance_measure()

        if value is not None:
            data = {
                'sensor_id': SENSOR_ID,
                'type': 'illuminance',
                'value': value
            }
            requests.post(f'http://{SERVER_ADDRESS}:{SERVER_PORT}/api/sensor-reading/', json=data, headers={'x-api-key': 'sensor'})
        else:
            print('Не удалось считать данные с датчика.')
        time.sleep(1)
except KeyboardInterrupt:
    print("Завершение работы...")
