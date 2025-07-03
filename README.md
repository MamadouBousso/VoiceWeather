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
