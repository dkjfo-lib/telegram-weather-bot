import requests
import os
import datetime


async def get_weather_test(city: str):
    API_KEY = os.getenv('OPEN_WEATHER_MAP_API')
    complete_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&cnt=1'
    response = requests.get(complete_url, params={'lang': 'ru'})
    x = response.json()
    print()
    print(x)
    print()
    code=x["cod"]
    if code != "200":
        return [x["message"]]
    timezone_s = x["city"]["timezone"]
    lat = round(x["city"]["coord"]["lat"], 2)
    lon = round(x["city"]["coord"]["lon"], 2)
    coords = f'latitude={lat}&longitude={lon}'
    dayStart = (datetime.datetime.utcnow() + datetime.timedelta(seconds=timezone_s)).strftime('%Y-%m-%d')
    dayEnd = (datetime.datetime.utcnow() + datetime.timedelta(days=3, seconds=timezone_s)).strftime('%Y-%m-%d')
    complete_url = f'https://api.open-meteo.com/v1/forecast?{coords}&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation_probability,precipitation,weathercode,windspeed_10m&daily=sunrise,sunset,uv_index_max,precipitation_sum&windspeed_unit=ms&start_date={dayStart}&end_date={dayEnd}&timezone=auto'
    response = requests.get(complete_url)
    data = response.json()
    print()
    print(dayStart)
    print(dayEnd)
    print()
    print(data)
    print()
    print()

    data_h = data["hourly"]
    data_day = data["daily"]
    data_count = len(data["hourly"]["time"])
    messages = []
    for day_id in range(0, int(data_count / 24)):
        message_text = f'{city}: {data_day["time"][day_id]}\n'
        sunrise = data_day["sunrise"][day_id][11:]
        sunset = data_day["sunset"][day_id][11:]
        uv_index = data_day["uv_index_max"][day_id]
        precipitation_sum = data_day["precipitation_sum"][day_id]
        message_text += f'🌄 {sunrise} 🌆 {sunset}\n'
        message_text += f'😎 {uv_index} 💧 {precipitation_sum} mm\n\n'
        for hour_id in range(24 * day_id, 24 * (day_id+1)):
            daytime = convert_to_ampm(data_h["time"][hour_id][11:-3])
            weather_emoji = get_weather_emoji_test(data_h["weathercode"][hour_id])
            temperature = round(data_h["temperature_2m"][hour_id])
            wind_speed = round(data_h["windspeed_10m"][hour_id])
            precipitation = data_h["precipitation"][hour_id]
            message_text += f'{weather_emoji} {daytime}\t'
            message_text += f'🌡 {temperature}°C 🌬 {wind_speed} m/s 💧 {precipitation} mm\n'
        messages.append(message_text)
    return messages


def convert_to_ampm(hour :str):
    hour = int(hour)
    if hour == 0:
        return '12 AM'
    elif hour < 12:
        return f'{hour} AM'
    elif hour == 12:
        return f'{hour} PM'
    else:
        return f'{hour-12} PM'
    

def get_weather_emoji_test(code: int) -> str:
    if code == 0:
        return "☀️"
    elif code == 2:
        return "⛅️"
    elif code == 2:
        return "🌥"
    elif code == 3:
        return "☁️"
    elif code <= 48:
        return "🌫"
    elif code <= 55:
        return "🌧"
    elif code <= 57:
        return "🌨"
    elif code <= 65:
        return "🌧"
    elif code <= 77:
        return "🌨"
    elif code <= 82:
        return "🌧"
    elif code <= 86:
        return "🌨"
    elif code <= 99:
        return "🌩"
    else:
        return code
