import math
import random
import time

import requests

SERVER_ADDRESS = 'localhost'
SERVER_PORT = '8000'
SENSOR_ID = f'iot-sensor-temperature-{random.randint(0, 1000)}'

i = 0
current_temperature = 20
max_temperature = 40


def get_temperature_measure():
    global current_temperature, i
    i += 2
    current_temperature = math.sin(i * 0.1) * max_temperature
    print(current_temperature)
    return current_temperature


try:
    while True:
        value = get_temperature_measure()

        if value is not None:
            data = {
                'sensor_id': SENSOR_ID,
                'type': 'temperature',
                'value': value
            }
            requests.post(f'http://{SERVER_ADDRESS}:{SERVER_PORT}/api/sensor-reading/', json=data, headers={'x-api-key': 'sensor'})
        else:
            print('Не удалось считать данные с датчика.')
        time.sleep(1)
except KeyboardInterrupt:
    print("Завершение работы...")
