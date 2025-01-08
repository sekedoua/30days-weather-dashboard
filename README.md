# 30 Days DevOps Challenge - Dashboard Météo
# Weather Data Collection System - DevOps Day 1 Challenge
# Day 1: Building a weather data collection system using AWS S3 and OpenWeather API

## Aperçu du projet
Ce projet est un système de collecte de données météorologiques qui démontre les principes fondamentaux de DevOps en combinant :
- Intégration d'API externes (API OpenWeather)
- Stockage dans le cloud (AWS S3)
- Infrastructure en tant que code
- Contrôle de version (Git)
- Développement Python
- Gestion des erreurs
- Gestion de l'environnement

## Caractéristiques du projet
- Récupère les données météorologiques en temps réel pour plusieurs villes
- Affiche la température (°F), l'humidité et les conditions météorologiques
- Stocke automatiquement les données météorologiques dans AWS S3
- Prend en charge le suivi de plusieurs villes
- Horodatage de toutes les données pour un suivi historique

## Architecture technique
-  Python 3.x
-   AWS (S3)
- **External API:** OpenWeather API
- **Dependencies:** 
  - boto3 (AWS SDK)
  - python-dotenv
  - requests

```markdown
## Structure du projet
weather-dashboard/
  src/
    __init__.py
    weather_dashboard.py
  tests/
  data/
  .env
  .gitignore
  requirements.txt

## Instructions de configuration
1. Clone the repository:
--bash
git clone https://github.com/sekedoua/30days-weather-dashboard.git

3. Install dependencies:
--bash
pip install -r requirements.txt

4. Configuration des variable d'environnement fichier ( fichier .env):
OPENWEATHER_API_KEY="votre_cle_API"
AWS_BUCKET_NAME="nom_de_votre_compartiment_S3"

4.Configure  de vos accès AWS :
--bash 
aws configure

5. Lancer l'application :
python src/weather_dashboard.py

Ce que j'ai appris

Création et gestion de buckets/compartiments AWS S3
Gestion des variables d'environnement pour des clés API sécurisées
Bonnes pratiques Python pour l'intégration d'API
Flux de travail Git pour le développement de projets
Gestion des erreurs dans les systèmes distribués
Gestion des ressources cloud

Future Enhancements

Add weather forecasting
Implement data visualization
Add more cities
Create automated testing
Set up CI/CD pipeline
