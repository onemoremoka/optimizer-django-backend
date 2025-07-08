### DEV Pipeline

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
 ```