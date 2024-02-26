# Utilisez l'image Python officielle comme base
FROM python:3.9

# Mise à jour du système et installation des dépendances
RUN apt-get update && apt-get install -y libpcap-dev && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez le code source de l'application dans le conteneur
COPY ApiWEB/Launcher.py ApiWEB/data_manager.py /app/

# Installation des dépendances 
RUN pip install --no-cache-dir -r requirements.txt

# Exposez le port sur lequel votre application Flask fonctionne
EXPOSE 5000

# Commande pour exécuter l'application Flask
CMD ["sh", "-c", "python3 Launcher.py & python3 data_manager.py"]
