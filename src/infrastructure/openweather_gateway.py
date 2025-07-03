import os
import requests

def get_weather_from_openweather(ville):
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        raise ValueError("La clé API OpenWeather n'est pas définie dans les variables d'environnement.")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ville}&appid={api_key}&units=metric&lang=fr"
    response = requests.get(url)
    if response.status_code != 200:
        return {"erreur": f"Impossible de récupérer la météo pour {ville}."}
    data = response.json()
    return {
        "ville": data.get("name") or ville or "Inconnu",
        "temperature": f"{data['main']['temp']}°C" if 'main' in data and 'temp' in data['main'] else "",
        "condition": data['weather'][0]['description'].capitalize() if 'weather' in data and data['weather'] else "",
        "vent": f"{data['wind']['speed']} km/h" if 'wind' in data and 'speed' in data['wind'] else "",
        "pays": data.get("sys", {}).get("country", "")
    }

def get_weather_by_coordinates(lat, lon, units="metric"):
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        raise ValueError("La clé API OpenWeather n'est pas définie dans les variables d'environnement.")
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={units}&lang=fr"
    response = requests.get(url)
    if response.status_code != 200:
        return {"erreur": f"Impossible de récupérer la météo pour les coordonnées {lat}, {lon}."}
    data = response.json()
    return {
        "latitude": lat,
        "longitude": lon,
        "temperature": f"{data['main']['temp']}°{'C' if units == 'metric' else 'F' if units == 'imperial' else 'K'}" if 'main' in data and 'temp' in data['main'] else "",
        "condition": data['weather'][0]['description'].capitalize() if 'weather' in data and data['weather'] else "",
        "ville": data.get("name", "Inconnu"),
        "pays": data.get("sys", {}).get("country", "")
    }

def get_weather_by_location(location, units="metric"):
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        raise ValueError("La clé API OpenWeather n'est pas définie dans les variables d'environnement.")
    # Géocodage
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={api_key}"
    geo_response = requests.get(geo_url)
    if geo_response.status_code != 200 or not geo_response.json():
        return {"erreur": f"Impossible de trouver les coordonnées pour '{location}'."}
    geo_data = geo_response.json()[0]
    lat = geo_data.get('lat')
    lon = geo_data.get('lon')
    if lat is None or lon is None:
        return {"erreur": f"Coordonnées non trouvées pour '{location}'."}
    # Appel météo
    meteo = get_weather_by_coordinates(lat, lon, units)
    meteo['ville'] = geo_data.get('name', location) or location or "Inconnu"
    meteo['pays'] = geo_data.get('country', meteo.get('pays', ""))
    meteo['latitude'] = lat
    meteo['longitude'] = lon
    return meteo 