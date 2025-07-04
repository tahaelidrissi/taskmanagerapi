# Image de base Python légère
FROM python:3.11-slim

# Définir le dossier de travail dans le conteneur
WORKDIR /app

# Copier requirements.txt en premier pour profiter du cache Docker
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le reste du projet dans le conteneur
COPY . .

# Exposer le port 8000 (celui de ton API)
EXPOSE 8000

# Commande pour lancer FastAPI via uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
