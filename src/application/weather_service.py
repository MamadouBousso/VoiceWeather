import os
from src.infrastructure.openweather_gateway import get_weather_from_openweather
from src.domaine.ports.weather_provider import WeatherProvider
from src.domaine.ports.llm_provider import LLMProvider
from src.domaine.entities.weather import WeatherInfo
from src.domaine.entities.llm_reply import LLMReply

def get_static_weather():
    return {
        "ville": "Paris",
        "temperature": "18°C",
        "condition": "Ensoleille",
        "vent": "10 km/h"
    }

class WeatherService:
    def __init__(self, weather_provider: WeatherProvider, llm_provider: LLMProvider):
        self.weather_provider = weather_provider
        self.llm_provider = llm_provider

    def get_weather_and_reply(self, location=None, lat=None, lon=None):
        weather: WeatherInfo = self.weather_provider.get_weather(location=location, lat=lat, lon=lon)
        reply: LLMReply = self.llm_provider.generate_reply(weather)
        return reply, weather

