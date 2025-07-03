from abc import ABC, abstractmethod
from src.domaine.entities.weather import WeatherInfo
from src.domaine.entities.llm_reply import LLMReply

class LLMProvider(ABC):
    @abstractmethod
    def generate_reply(self, weather: WeatherInfo) -> LLMReply:
        pass 