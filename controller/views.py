import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import SensorReading, HoodActuatorConfig, LampActuatorConfig, WateringActuatorConfig, TemperatureNotificationConfig
import plotly.graph_objs as go
import plotly.offline as pyo
from datetime import datetime, timedelta

from .telegram import send_message


def humidity_chart(request):
    # Извлекаем данные из базы данных
    data = SensorReading.objects.filter(reading_type='humidity').filter(timestamp__gt=datetime.now() - timedelta(minutes=10)).order_by('timestamp')
    config = HoodActuatorConfig.objects.last()
    hood_speed = config.hood_speed

    # Подготавливаем данные для графика
    humidity_values = [d.reading_value for d in data]
    timestamps = [d.timestamp for d in data]

    last_humidity = round(humidity_values[-1], 2)
    last_timestamp = timestamps[-1]

    hood_enabled = last_humidity > config.min_value

    # Создаем график
    trace = go.Scatter(x=timestamps, y=humidity_values, mode='lines+markers', name='Humidity')
    layout = go.Layout(title='Влажность от времени', xaxis=dict(title='Дата и время'), yaxis=dict(title='Влажность (%)'))
    fig = go.Figure(data=[trace], layout=layout)
    fig.add_hline(y=config.min_value, line_color='Red')

    # Генерируем HTML-код для графика
    graph_html = pyo.plot(fig, include_plotlyjs=False, output_type='div')

    # Отправляем график в контексте шаблона
    return render(request, 'humidity_chart.html', {
        'graph_html': graph_html,
        'last_humidity': last_humidity,
        'last_timestamp': last_timestamp,
        'is_hood_enabled': hood_enabled,
        'hood_speed': hood_speed
    })


def illuminance_chart(request):
    # Извлекаем данные из базы данных
    data = SensorReading.objects.filter(reading_type='illuminance').filter(timestamp__gt=datetime.now() - timedelta(minutes=10)).order_by('timestamp')
    config = LampActuatorConfig.objects.last()

    # Подготавливаем данные для графика
    illuminance_values = [d.reading_value for d in data]
    timestamps = [d.timestamp for d in data]

    last_illuminance = round(illuminance_values[-1], 2)
    last_timestamp = timestamps[-1]

    lamp_enabled = last_illuminance <= config.min_value

    # Создаем график
    trace = go.Scatter(x=timestamps, y=illuminance_values, mode='lines+markers', name='Illuminance')
    layout = go.Layout(title='Освещенность от времени', xaxis=dict(title='Дата и время'), yaxis=dict(title='Освещенность (лк)'))
    fig = go.Figure(data=[trace], layout=layout)
    fig.add_hline(y=config.min_value, line_color='Red')

    # Генерируем HTML-код для графика
    graph_html = pyo.plot(fig, include_plotlyjs=False, output_type='div')

    # Отправляем график в контексте шаблона
    return render(request, 'illuminance_chart.html', {
        'graph_html': graph_html,
        'last_illuminance': last_illuminance,
        'last_timestamp': last_timestamp,
        'is_lamp_enabled': lamp_enabled
    })


def moisture_chart(request):
    # Извлекаем данные из базы данных
    data = SensorReading.objects.filter(reading_type='moisture').filter(timestamp__gt=datetime.now() - timedelta(minutes=10)).order_by('timestamp')
    config = WateringActuatorConfig.objects.last()

    # Подготавливаем данные для графика
    illuminance_values = [d.reading_value for d in data]
    timestamps = [d.timestamp for d in data]

    last_illuminance = round(illuminance_values[-1], 2)
    last_timestamp = timestamps[-1]

    lamp_enabled = last_illuminance <= config.min_value

    # Создаем график
    trace = go.Scatter(x=timestamps, y=illuminance_values, mode='lines+markers', name='Soil moisture')
    layout = go.Layout(title='Влажность почвы от времени', xaxis=dict(title='Дата и время'), yaxis=dict(title='Влажность почвы (%)'))
    fig = go.Figure(data=[trace], layout=layout)
    fig.add_hline(y=config.min_value, line_color='Green')
    fig.add_hline(y=config.max_value, line_color='Red')

    # Генерируем HTML-код для графика
    graph_html = pyo.plot(fig, include_plotlyjs=False, output_type='div')

    # Отправляем график в контексте шаблона
    return render(request, 'moisture_chart.html', {
        'graph_html': graph_html,
        'last_illuminance': last_illuminance,
        'last_timestamp': last_timestamp,
        'is_lamp_enabled': lamp_enabled
    })

def temperature_chart(request):
    # Извлекаем данные из базы данных
    data = SensorReading.objects.filter(reading_type='temperature').filter(timestamp__gt=datetime.now() - timedelta(minutes=10)).order_by('timestamp')
    configs = TemperatureNotificationConfig.objects.all()

    # Подготавливаем данные для графика
    illuminance_values = [d.reading_value for d in data]
    timestamps = [d.timestamp for d in data]

    last_illuminance = round(illuminance_values[-1], 2)
    last_timestamp = timestamps[-1]

    # Создаем график
    trace = go.Scatter(x=timestamps, y=illuminance_values, mode='lines+markers', name='Temperature')
    layout = go.Layout(title='Температура от времени', xaxis=dict(title='Дата и время'), yaxis=dict(title='Температура (°С)'))
    fig = go.Figure(data=[trace], layout=layout)

    for config in configs:
        if config.is_excess:
            fig.add_hline(y=config.threshold, line_color='Red')
        else:
            fig.add_hline(y=config.threshold, line_color='Blue')

    # Генерируем HTML-код для графика
    graph_html = pyo.plot(fig, include_plotlyjs=False, output_type='div')

    # Отправляем график в контексте шаблона
    return render(request, 'temperature_chart.html', {
        'graph_html': graph_html,
        'last_illuminance': last_illuminance,
        'last_timestamp': last_timestamp
    })


@csrf_exempt
def add_sensor_reading(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))

        if body['type'] == 'temperature':
            last = SensorReading.objects.filter(reading_type='temperature').order_by('timestamp').last()

            if last is not None:
                last = last.reading_value
                is_excess = body['value'] >= last
                configs = TemperatureNotificationConfig.objects.all()
                for config in configs:
                    if is_excess and config.is_excess and last <= config.threshold <= body['value']:
                        send_message(config.text + f"\nТемпература: {body['value']:.0f} °С")
                    elif not is_excess and not config.is_excess and last >= config.threshold >= body['value']:
                        send_message(config.text + f"\nТемпература: {body['value']:.0f} °С")

        SensorReading(reading_type=body['type'], reading_value=body['value'], timestamp=datetime.now()).save()
        return JsonResponse({'success': True}, safe=False)


@csrf_exempt
def get_hood_speed(request):
    if request.method == 'GET':
        last = SensorReading.objects.filter(reading_type='humidity').order_by('timestamp').last()
        config = HoodActuatorConfig.objects.last()
        hood_speed = config.hood_speed
        if last.reading_value <= config.min_value:
            hood_speed = 0
        return JsonResponse({'speed': hood_speed}, safe=False)


@csrf_exempt
def get_watering_state(request):
    if request.method == 'GET':
        result_set = SensorReading.objects.filter(reading_type='moisture').order_by('-timestamp')[:2]
        if len(result_set) < 1:
            return JsonResponse({'state': 'off'}, safe=False)

        config = WateringActuatorConfig.objects.last()
        current = result_set[0].reading_value
        if current >= config.max_value:
            return JsonResponse({'state': 'off'}, safe=False)
        elif current >= config.min_value:
            if len(result_set) > 1:
                previous = result_set[1].reading_value
                state = 'on' if previous <= current else 'off'
                return JsonResponse({'state': state}, safe=False)
            else:
                return JsonResponse({'state': 'off'}, safe=False)
        else:
            return JsonResponse({'state': 'on'}, safe=False)
