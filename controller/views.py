from django.shortcuts import render
from .models import SensorReading, HoodActuatorConfig
import plotly.graph_objs as go
import plotly.offline as pyo
from datetime import datetime, timedelta


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
