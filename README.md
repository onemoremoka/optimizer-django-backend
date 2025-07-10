# Optimizer Django Backend

Este proyecto es un MVP de backend en Django framework diseñado para resolver problemas de optimización lineal entera utilizando Pyomo y GLPK como solver.

## ⚙️ Tecnologías

- **Django**: Framework web para construir aplicaciones backend.
- **Pyomo**: Para modelar problemas de optimización.
- **GLPK**: Solver de programación lineal.

## 🧪 Config DEV

```bash
# para una prueba rapida (docker-compose en caso de prod)
pyenv local 3.10.14
python3 -m venv .venv
source .venv/bin/activate

# dependencias
pip install -r requirements.txt
sudo apt install glpk-utils

# (opcional) si existen secretkeys u info sensible
cp .env.example .env

# configuracion modelo de datos
python manage.py makemigrations optimizer
python manage.py migrate

# runserver
python manage.py runserver
```

```bash
# unicamente para validar la logica del pipeline
python3 main.py
```

```bash
# test unitarios
python3 -m pip install -r requirements-dev.txt
pytest
```

**Acceso:** `http://localhost:8000`

**Notas:**
- El proyecto considera tres Handlers:
  - `TerminalResultsHandler`: desplegar información por terminal. manejado en el main.py
  - `CSVResultsHandler`: almacenar resultados en un archivo .CSV. manejado en el main.py
  - `HtmlResultsHandler`: Estructurar datos para incrustar en HTML. manejado en el view.py

- Se utiliza una modelo de datos simple para almacenar los resultados de los experimentos. Se debe migrar el modelo de datos con `python manage.py makemigrations optimizer` y `python manage.py migrate`.


## 🚀 Deployment

```bash
docker compose up --build
```

El proyecto final se ejecuta dentro de contenedores. Usa Dockerfile para construir la aplicación o docker-compose para levantar el servicio backend con servicios complementarios (Grafana, Prometheus, cadvisor).

Puertos expuestos:
- 8000: puerto del servicio web: Aplicación Django
- 3000: puerto de Grafana: Visualización de datos
- 9090: puerto de Prometheus: Recolección de métricas
- 8080: puerto de cAdvisor: Monitoreo de contenedores

## ⚠️ Disclaimer
Mas comandos detallados que anote mientras iba desarrollando [devpipeline.md](docs/devpipeline.md)

