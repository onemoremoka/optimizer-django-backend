FROM python:3.10-slim

# evitar crear archivos .pyc (bytecode compilados)
ENV PYTHONDONTWRITEBYTECODE=1

# aqui creo un usuario no root para ejecutar la app
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    glpk-utils \
    nano \
    libglpk-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# cambio el permiso sobre el dir /app para que el usuario appuser pueda acceder
RUN chown -R appuser:appgroup /app

# cambio al usuario appuser
USER appuser

# Se declara que se expone el puerto 8000
EXPOSE 8000

# entrypoint del dockerfile
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
