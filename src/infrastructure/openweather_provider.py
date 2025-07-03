import os
import requests
from src.domaine.entities.weather import WeatherInfo
from src.domaine.ports.weather_provider import WeatherProvider

class OpenWeatherProvider(WeatherProvider):
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        if not self.api_key:
            raise ValueError("La clé API OpenWeather n'est pas définie dans les variables d'environnement.")

    def get_weather(self, location: str = None, lat: float = None, lon: float = None) -> WeatherInfo:
        if location:
            # Géocodage
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={self.api_key}"
            geo_response = requests.get(geo_url)
            if geo_response.status_code != 200 or not geo_response.json():
                raise ValueError(f"Impossible de trouver les coordonnées pour '{location}'.")
            geo_data = geo_response.json()[0]
            lat = geo_data.get('lat')
            lon = geo_data.get('lon')
            ville = geo_data.get('name', location) or location or "Inconnu"
            pays = geo_data.get('country', "")
        else:
            ville = "Inconnu"
            pays = ""
        if lat is None or lon is None:
            raise ValueError("Coordonnées non trouvées.")
        # Appel météo
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric&lang=fr"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"Impossible de récupérer la météo pour les coordonnées {lat}, {lon}.")
        data = response.json()
        return WeatherInfo(
            ville = data.get("name", ville),
            pays = data.get("sys", {}).get("country", pays),
            temperature = f"{data['main']['temp']}°C" if 'main' in data and 'temp' in data['main'] else "",
            condition = data['weather'][0]['description'].capitalize() if 'weather' in data and data['weather'] else "",
            vent = f"{data['wind']['speed']} km/h" if 'wind' in data and 'speed' in data['wind'] else "",
            latitude = lat,
            longitude = lon
        ) 