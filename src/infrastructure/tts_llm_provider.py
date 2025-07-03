import os
import requests
import threading
from src.domaine.entities.weather import WeatherInfo
from src.domaine.entities.llm_reply import LLMReply
from src.domaine.ports.llm_provider import LLMProvider
from src.infrastructure.openai_llm_provider import OpenAILLMProvider

class TTSLLMProvider(LLMProvider):
    """
    Fournisseur LLM qui génère le texte avec OpenAI puis la voix avec ElevenLabs (API HTTP).
    La génération audio est lancée dans un thread pour que le texte s'affiche immédiatement.

    Paramètres du constructeur :
    - tts_lang : langue cible (ex : 'fr')
    - voice : nom exact ou voice_id d'une voix ElevenLabs (doit être activée sur votre compte)
      Si non fourni, la voix est lue depuis la variable d'environnement ELEVENLABS_VOICE.
    - model : modèle ElevenLabs à utiliser (par défaut 'eleven_multilingual_v2')

    Nécessite la variable d'environnement ELEVENLABS_API_KEY.
    """
    def __init__(self, tts_lang='fr', voice=None, model='eleven_multilingual_v2'):
        self.text_llm = OpenAILLMProvider()
        self.tts_lang = tts_lang
        self.audio_dir = 'static/audio'
        os.makedirs(self.audio_dir, exist_ok=True)
        self.voice = voice or os.getenv("ELEVENLABS_VOICE")
        self.model = model
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY n'est pas défini dans les variables d'environnement.")
        if not self.voice:
            raise ValueError("Aucune voix ElevenLabs n'est définie. Passez-la en paramètre ou via ELEVENLABS_VOICE.")

    def _generate_audio(self, texte, audio_path):
        """
        Lance la génération audio via l'API ElevenLabs (HTTP POST) et sauvegarde le fichier mp3.
        """
        print(f"[TTSLLMProvider] Début génération audio pour {audio_path}")
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice}"
            headers = {
                "xi-api-key": self.api_key,
                "Content-Type": "application/json"
            }
            data = {
                "text": texte,
                "model_id": self.model,
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
            }
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            with open(audio_path, "wb") as f:
                f.write(response.content)
            print(f"[TTSLLMProvider] Audio généré : {audio_path}")
        except Exception as e:
            print(f"[TTSLLMProvider] Erreur génération audio : {e}")

    def generate_reply(self, weather: WeatherInfo) -> LLMReply:
        """
        Génère la réponse texte (OpenAI) et lance la génération audio ElevenLabs en tâche de fond.
        Retourne immédiatement le texte et le chemin du fichier audio (qui sera prêt dès que le thread a fini).
        """
        llm_reply = self.text_llm.generate_reply(weather)
        texte = llm_reply.texte
        filename = f"weather_{weather.ville}_{weather.latitude}_{weather.longitude}.mp3".replace(' ', '_')
        audio_path = os.path.join(self.audio_dir, filename)
        threading.Thread(target=self._generate_audio, args=(texte, audio_path), daemon=True).start()
        return LLMReply(texte=texte, source="openai+elevenlabs", audio_path=audio_path) 