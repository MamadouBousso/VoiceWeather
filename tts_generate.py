import sys
import os
from elevenlabs import generate, save, set_api_key

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 tts_generate.py <texte> <audio_path> <langue>")
        sys.exit(1)
    texte = sys.argv[1]
    audio_path = sys.argv[2]
    tts_lang = sys.argv[3]

    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("ELEVENLABS_API_KEY n'est pas défini dans les variables d'environnement.")
        sys.exit(1)
    set_api_key(api_key)

    # Utiliser une voix française par défaut (ex: "Antoine" ou "Claire")
    # Tu peux changer le voice_id selon tes préférences sur https://elevenlabs.io/voice-lab
    voice = "EXAVITQu4vr4xnSDxMaL"  # ou "Claire", "Eloise", etc.
    audio = generate(
        text=texte,
        voice=voice,
        model="eleven_multilingual_v2"
    )
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    save(audio, audio_path) 