from flask import Flask, request, jsonify, render_template, url_for, send_file
from src.infrastructure.openweather_provider import OpenWeatherProvider
from src.infrastructure.tts_llm_provider import TTSLLMProvider
from src.infrastructure.openai_llm_provider import OpenAILLMProvider
from src.application.weather_service import WeatherService
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

# Injection des providers
weather_provider = OpenWeatherProvider()
tts_llm_provider = TTSLLMProvider()
text_llm_provider = OpenAILLMProvider()
weather_service = WeatherService(weather_provider, tts_llm_provider)

def country_flag(country_code):
    if not country_code or len(country_code) != 2:
        return ""
    return chr(0x1F1E6 + ord(country_code.upper()[0]) - ord('A')) + \
           chr(0x1F1E6 + ord(country_code.upper()[1]) - ord('A'))

app.jinja_env.filters['country_flag'] = country_flag

@app.route('/')
def home():
    return render_template('weather_form.html')

@app.route('/weather/location')
def weather_by_location():
    location = request.args.get('location')
    audio = request.args.get('audio') == '1'
    llm_provider = tts_llm_provider if audio else text_llm_provider
    weather_service = WeatherService(weather_provider, llm_provider)
    if not location:
        return render_template('weather.html', reponse="Aucune ville sélectionnée.", donnees={}, audio_url=None), 400
    reply, weather = weather_service.get_weather_and_reply(location=location)
    if audio and reply.audio_path:
        return send_file(reply.audio_path, mimetype='audio/mpeg', as_attachment=False)
    audio_url = None
    if reply.audio_path:
        audio_url = url_for('static', filename=os.path.relpath(reply.audio_path, 'static'))
    return render_template('weather.html', reponse=reply.texte, donnees=weather.__dict__, audio_url=audio_url)

@app.route('/weather')
def weather():
    ville = request.args.get('ville', 'Paris')
    audio = request.args.get('audio') == '1'
    llm_provider = tts_llm_provider if audio else text_llm_provider
    weather_service = WeatherService(weather_provider, llm_provider)
    reply, weather = weather_service.get_weather_and_reply(location=ville)
    if audio and reply.audio_path:
        return send_file(reply.audio_path, mimetype='audio/mpeg', as_attachment=False)
    audio_url = None
    if reply.audio_path:
        audio_url = url_for('static', filename=os.path.relpath(reply.audio_path, 'static'))
    return render_template('weather.html', reponse=reply.texte, donnees=weather.__dict__, audio_url=audio_url)

@app.route('/weather/coordinates')
def weather_by_coordinates():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    audio = request.args.get('audio') == '1'
    llm_provider = tts_llm_provider if audio else text_llm_provider
    weather_service = WeatherService(weather_provider, llm_provider)
    units = request.args.get('units', 'metric')
    if not lat or not lon:
        return render_template('weather.html', reponse="Les paramètres 'lat' et 'lon' sont obligatoires.", donnees={}, audio_url=None), 400
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return render_template('weather.html', reponse="Les paramètres 'lat' et 'lon' doivent être des nombres.", donnees={}, audio_url=None), 400
    reply, weather = weather_service.get_weather_and_reply(lat=lat, lon=lon)
    if audio and reply.audio_path:
        return send_file(reply.audio_path, mimetype='audio/mpeg', as_attachment=False)
    audio_url = None
    if reply.audio_path:
        audio_url = url_for('static', filename=os.path.relpath(reply.audio_path, 'static'))
    return render_template('weather.html', reponse=reply.texte, donnees=weather.__dict__, audio_url=audio_url)

if __name__ == '__main__':
    app.run(debug=True) 