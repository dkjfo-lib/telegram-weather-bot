import requests
import os


async def get_weather_test(city: str):
    coords = 'latitude=44.80&longitude=20.47'
    complete_url = f'https://api.open-meteo.com/v1/forecast?{coords}&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation_probability,precipitation,weathercode,windspeed_10m&daily=sunrise,sunset,uv_index_max,precipitation_sum&windspeed_unit=ms&start_date=2023-04-05&end_date=2023-04-07&timezone=auto'
    response = requests.get(complete_url)
    data = response.json()
    print()
    print()
    print(data)
    print()
    print()

    data_h = data["hourly"]
    data_day = data["daily"]
    data_count = len(data["hourly"]["time"])
    embeds = []
    for day_id in range(0, int(data_count / 24)):
        embed = discord.Embed(title=f'{data_day["time"][day_id]}')
        sunrise = data_day["sunrise"][day_id][11:]
        sunset = data_day["sunset"][day_id][11:]
        uv_index = data_day["uv_index_max"][day_id]
        precipitation_sum = data_day["precipitation_sum"][day_id]
        name = f'🌄 {sunrise} 🌆 {sunset}'
        value = f'😎 {uv_index} 💧 {precipitation_sum} mm'
        embed.add_field(name=name, value=value, inline=False)
        for hour_id in range(24 * day_id, 24 * (day_id+1)):
            daytime = convert_to_ampm(data_h["time"][hour_id][11:-3])
            weather_emoji = get_weather_emoji_test(data_h["weathercode"][hour_id])
            temperature = round(data_h["temperature_2m"][hour_id])
            wind_speed = round(data_h["windspeed_10m"][hour_id])
            precipitation = data_h["precipitation"][hour_id]
            name = f'{weather_emoji} {daytime}'
            value = f'🌡 {temperature}°C\n🌬 {wind_speed} m/s\n💧 {precipitation} mm'
            embed.add_field(name=name, value=value, inline=True)
        embeds.append(embed)
    return message_model(text = f"Погода в {city}", embeds=embeds)


async def get_weather(city: str):
    API_KEY = os.getenv('OPEN_WEATHER_MAP_API')
    complete_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&cnt=9'
    response = requests.get(complete_url, params={'lang': 'ru'})
    x = response.json()
    print(x)

    embed = discord.Embed(title=f"Погода в {city}")
    for wt in x["list"]:
        name = f'{wt["dt_txt"][-9:-3]} {wt["weather"][0]["description"]} {get_weather_emoji(wt["weather"][0]["icon"])}'

        perception = '0 '
        if "rain" in wt:
            perception = f'{wt["rain"]["3h"]}💧'
        elif "snow" in wt:
            perception = f'{wt["snow"]["3h"]}❄'
        value = f'{round(wt["main"]["temp_min"])}-{round(wt["main"]["temp_max"])}°C    {round(wt["wind"]["speed"])}m/s    {perception}mm/3h'

        embed.add_field(name=name, value=value)
    return message_model(embed=embed)

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
    
def get_weather_emoji(icon: str) -> str:
    icon = icon[:-1]
    if icon == '01':
        return ":sunny:"
    elif icon == '02':
        return "🌤"
    elif icon == '03':
        return ":cloud:"
    elif icon == '04':
        return "🌥"
    elif icon == '09':
        return "🌧"
    elif icon == '10':
        return "🌧"
    elif icon == '11':
        return "🌩"
    elif icon == '13':
        return "🌨"
    elif icon == '50':
        return "🌫"
    else:
        return icon


def get_weather_emoji_test(code: int) -> str:
    if code == 0:
        return ":sunny:"
    elif code == 2:
        return "🌤"
    elif code == 2:
        return "🌥"
    elif code == 3:
        return ":cloud:"
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
