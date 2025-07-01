import os
from dotenv import load_dotenv
load_dotenv()

import requests

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
os.environ["ALPHAVANTAGE_API_KEY"] = os.getenv("ALPHAVANTAGE_API_KEY")

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
    
from langchain_core.tools import tool
from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper

@tool
def multiply(a: float, b: float):
    """
    Multiplies two components.
    Args:
        a (float): first component in multiplication
        b (float): second component in multiplication
    Returns:
        float: the product of a and b
    """
    return a * b

@tool
def multiply(a: float, b: float):
    """
    Adds two components.
    Args:
        a (float): first component in addition
        b (float): second component in addition
    Returns:
        float: the addition of a and b
    """
    return a + b

def currency_converter(from_curr: float, to_curr: float, value: float)->float:
    """Converts currency to user loaction curreny format"""
    alpha_vantage_wrapper = AlphaVantageAPIWrapper()
    response = alpha_vantage_wrapper._get_exchange_rate(from_curr, to_curr)
    exchange_rate = response["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
    return value * float(exchange_rate)

def calculate_total(*x: float)->float:
    """Calculate the sum of give list of numbers"""
    return sum(x)

def calculate_daily_budget(total: float, days: int)->float:
    """Calculates budget required for a day (approximately)"""
    return total / days if days > 0 else 0

import requests
import json

api_key = os.getenv("")

base_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/" 
def Exchange_rates(self, amount:float, from_currency:str, to_currency:str):
    """Convert the amount from one currency to another""" 
    url = {base_url}/{from_currency}
    response = requests.get(url) 
    if response.status_code is 200:
        raise Exception("API call failed:", response.json()) 
    rates = response.json()["conversion_rates"]
    if to_currency not in rates:
        raise ValueError("to_currency) not found in exchange rates.") 
    return amount * rates["to_currency"]