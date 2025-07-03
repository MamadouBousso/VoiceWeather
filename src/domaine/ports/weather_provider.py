from abc import ABC, abstractmethod
from src.domaine.entities.weather import WeatherInfo

class WeatherProvider(ABC):
    @abstractmethod
    def get_weather(self, location: str = None, lat: float = None, lon: float = None) -> WeatherInfo:
        pass 