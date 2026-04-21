# ============================================================================
# IA FINDER - DOCKERFILE PRODUCTION
# ============================================================================

FROM python:3.11-slim

# Métadonnées
LABEL maintainer="support@ia-finder.com"
LABEL version="2.0.0"
LABEL description="IA Finder - Production Ready RAG System"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Dossier de travail
WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copie des fichiers de dépendances
COPY backend/requirements.txt .

# Installation des dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn gevent

# Copie du code source
COPY backend/app.py .
COPY backend/modules/ ./modules/
COPY frontend/index.html .

# Création des dossiers nécessaires
RUN mkdir -p uploads logs data && \
    chmod -R 755 uploads logs data

# Utilisateur non-root pour la sécurité
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Port exposé
EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Commande de démarrage (production avec Gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "--worker-class", "gevent", "--timeout", "120", "--access-logfile", "logs/access.log", "--error-logfile", "logs/error.log", "--log-level", "info", "app:app"]