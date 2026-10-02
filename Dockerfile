FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# System dependencies for numpy/scipy/pandas + PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    gfortran \
    libpq-dev \
    libopenblas-dev \
    liblapack-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy backend source
COPY backend/ /app/

# Collect static files (optional)
RUN python manage.py collectstatic --noinput || true

# Expose Railway's dynamic port
ENV PORT=8000
EXPOSE 8000

# Start command: migrate, load data, then gunicorn
CMD python manage.py migrate --noinput && \
    python manage.py load_fuel_data --limit 100 || true && \
    gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
