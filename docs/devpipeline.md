# DEV Pipeline

Pipeline de creación y configuración del proyecto: 

```bash
# creación entorno de trabajo
pyenv local 3.10.14
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements-dev.txt


# configuracion inicial:
django-admin startproject config . # con esto comando creo la configuracion global del proyecto
python manage.py migrate # crea la estructura basica para la base de datos en un .sqlite
python manage.py createsuperuser # creo un superusuario para poder acceder al admin de django

# crear app
python manage.py startapp core # creo la app core

# una vez creada el modelo de datos se debe migrar con el manage.py
python manage.py makemigrations optimizer
python manage.py migrate

```

# Deployment
```bash
# esto para levantar unicamente el dockerfile del backend

# construir la imagen
docker build -t optimizer-backend .

# (opcional) subir la imagen a dockerhub
docker tag optimizer-backend **user**/optimizer-backend:latest

 # creo una instancia del contenedor
docker run --rm --name optimizer-backend -p 8000:8000 optimizer-backend
```

```bash
# y esto para levantar todos los servicios
docker-compose up --build
```

# Otros comandos utiles

```bash
# para eliminar los registros de la DB
python manage.py shell

# dentro del shell
from optimizer.models import OptimizationResult
OptimizationResult.objects.all().delete()
```

```bash
# descargar templates para grafana
curl -s https://grafana.com/api/dashboards/11074/revisions/1/download -o deployments/grafana/docker_monitoring.

curl -s https://grafana.com/api/dashboards/14282/revisions/1/download -o deployments/grafana/docker_monitoring.json

# reemplazar variables de entorno en el template de grafana
sed -i 's/\${DS_PROMETHEUS[^}]*/Prometheus/g' deployments/grafana/docker_monitoring.json
```

