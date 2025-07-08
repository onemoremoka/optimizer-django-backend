# Optimizer Django Backend

MVP Django backend para resolver problema de optimizacion de produccion utilizando Pyomo y GLPK.

## Config dev

```bash
# en caso de desarrollo rapido (docker-compose en otro caso)
pyenv local 3.10.14
python3 -m venv .venv
source .venv/bin/activate

# dependencias
pip install -r requirements.txt
sudo apt install glpk-utils
cp .env.example .env

# runserver
python manage.py runserver
```

**Acceso:** http://localhost:8000

## Deployment

El proyecto final se ejecuta dentro de contenedores. Usa Dockerfile para construir la aplicación y docker-compose para levantar servicios complementarios. 
