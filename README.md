## Configuration de la clé API OpenWeather

Pour utiliser la fonction dynamique de récupération de la météo, vous devez obtenir une clé API sur https://openweathermap.org/ et l'ajouter à vos variables d'environnement :

Sous macOS/Linux :
```bash
export OPENWEATHER_API_KEY=VOTRE_CLE_API
```

Sous Windows (cmd) :
```cmd
set OPENWEATHER_API_KEY=VOTRE_CLE_API
```

Remplacez `VOTRE_CLE_API` par votre clé personnelle.

**Note :** Le fichier `.env` (où vous pouvez stocker votre clé API) est ignoré par git pour des raisons de sécurité. Pensez à le créer localement si besoin.

# Synthèse vocale avec ElevenLabs (TTS)

## Fonctionnement général

Ce projet utilise OpenAI pour générer le texte météo, puis ElevenLabs (API HTTP) pour générer la voix correspondante. La génération audio est asynchrone : le texte s'affiche immédiatement, et le lecteur audio apparaît dès que le fichier est prêt.

## Prérequis

- Python 3.8+
- `requests` (installé automatiquement)
- Un compte ElevenLabs avec une clé API valide

## Étapes d'installation et de configuration

1. **Installer les dépendances**
   ```bash
   pip install requests
   ```

2. **Créer un compte sur [https://elevenlabs.io/](https://elevenlabs.io/) et récupérer votre clé API**

3. **Définir les variables d'environnement**
   - Dans un fichier `.env` à la racine du projet :
     ```env
     ELEVENLABS_API_KEY=VOTRE_CLE_API
     ELEVENLABS_VOICE=VOTRE_VOICE_ID_OU_NOM
     ```
   - `ELEVENLABS_VOICE` doit être le nom exact ou le voice_id d'une voix activée sur votre compte. Pour lister vos voix :
     ```python
     import os, requests
     api_key = os.getenv("ELEVENLABS_API_KEY")
     url = "https://api.elevenlabs.io/v1/voices"
     headers = {"xi-api-key": api_key}
     resp = requests.get(url, headers=headers)
     for v in resp.json()["voices"]:
         print(f"{v['name']} : {v['voice_id']}")
     ```

4. **Lancer l'application**
   ```bash
   python app.py
   ```

## Fonctionnement asynchrone

- Le texte météo est généré et affiché immédiatement.
- La génération audio ElevenLabs est lancée dans un thread séparé (asynchrone).
- Le lecteur audio sur la page web vérifie régulièrement si le fichier mp3 est prêt et l'affiche dès que possible.

## Personnalisation

- Pour changer la voix, modifiez la variable d'environnement `ELEVENLABS_VOICE` ou passez le voice_id/nouveau nom lors de l'instanciation de `TTSLLMProvider`.
- Pour changer le modèle ElevenLabs, modifiez le paramètre `model` du provider (par défaut `eleven_multilingual_v2`).

## Gestion des erreurs

- Si la clé API ou la voix n'est pas définie, une erreur explicite est levée au démarrage.
- Si la génération audio échoue (mauvais voice_id, quota, etc.), l'erreur est loggée côté serveur, mais le texte reste affiché à l'utilisateur.

## Exemple d'utilisation dans le code

```python
from src.infrastructure.tts_llm_provider import TTSLLMProvider
provider = TTSLLMProvider(voice="EXAVITQu4vr4xnSDxMaL")  # ou nom exact de la voix
```

---

Pour toute question ou problème, consultez la documentation ElevenLabs ou contactez le mainteneur du projet.
