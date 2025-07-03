import os
import openai
from src.domaine.entities.weather import WeatherInfo
from src.domaine.entities.llm_reply import LLMReply
from src.domaine.ports.llm_provider import LLMProvider

class OpenAILLMProvider(LLMProvider):
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("La clé API OpenAI n'est pas définie dans les variables d'environnement.")
        openai.api_key = self.api_key

    def generate_reply(self, weather: WeatherInfo) -> LLMReply:
        prompt = (
            f"Voici les informations météo :\n"
            f"Ville : {weather.ville}\n"
            f"Pays : {weather.pays}\n"
            f"Latitude : {weather.latitude}\n"
            f"Longitude : {weather.longitude}\n"
            f"Température : {weather.temperature}\n"
            f"Condition : {weather.condition}\n"
            f"Vent : {weather.vent}\n"
            f"Rédige une réponse sympathique et concise pour un utilisateur français."
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant météo amical."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        texte = response.choices[0].message.content.strip()
        return LLMReply(texte=texte, source="openai") 