import os
from dotenv import load_dotenv
load_dotenv()

import requests

def get_weather_from_weatherapi(city: str, WEATHER_API_KEY: str) -> str:
    """A weather information provider"""
    try:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}&days=3&aqi=no&alerts=no"
        response = requests.get(url)
        
        # Ensure valid JSON
        if response.status_code != 200:
            return f"❗ API request failed with status code {response.status_code}"
        
        data = response.json()

        if "error" in data:
            return f"❗ API Error: {data['error'].get('message', 'Unknown error')}"

        location = data["location"]
        current = data["current"]
        forecast = data["forecast"]["forecastday"]

        report = (
            f"📍 {location['name']}, {location['country']}\n"
            f"🌡️ Temp: {current['temp_c']}°C (Feels like {current['feelslike_c']}°C)\n"
            f"💧 Humidity: {current['humidity']}% | ☁️ Cloud: {current['cloud']}%\n"
            f"🌬️ Wind: {current['wind_kph']} kph\n"
            f"🌤️ Condition: {current['condition']['text']}\n\n"
            f"🗓️ Forecast:\n"
        )

        for day in forecast:
            date = day["date"]
            day_data = day["day"]
            report += (
                f"{date}: 🌡️ {day_data['avgtemp_c']}°C, 🌧️ {day_data['condition']['text']}, "
                f"💧 Humidity: {day_data['avghumidity']}%, 🌬️ Wind: {day_data['maxwind_kph']} kph\n"
            )

        return report

    except Exception as e:
        return f"❗ Error: {str(e)}"