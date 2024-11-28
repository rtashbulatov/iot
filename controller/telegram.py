from iot.settings import TELEGRAM_CHAT_ID, TELEGRAM_TOKEN
import requests


def send_message(text):
    if TELEGRAM_CHAT_ID is None or TELEGRAM_TOKEN is None:
        raise AttributeError("TELEGRAM_CHAT_ID or TELEGRAM_TOKEN not defined")

    requests.post(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={text}')
