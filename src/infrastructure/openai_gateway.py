import os
import openai

def generate_weather_reply(weather_obj):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = (
        f"Voici les informations météo :\n"
        f"Ville : {weather_obj.get('ville', 'Inconnu')}\n"
        f"Latitude : {weather_obj.get('latitude', '')}\n"
        f"Longitude : {weather_obj.get('longitude', '')}\n"
        f"Température : {weather_obj.get('temperature', '')}\n"
        f"Condition : {weather_obj.get('condition', '')}\n"
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
    return response.choices[0].message.content.strip() 