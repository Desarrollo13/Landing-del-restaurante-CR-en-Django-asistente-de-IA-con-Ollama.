#!/usr/bin/env bash
# Script de build para Render: instala dependencias, recoge estáticos y migra.
set -o errexit

pip install -r requirements.txt

python backend/manage.py collectstatic --noinput
python backend/manage.py migrate --noinput

# Crea/actualiza el superusuario a partir de las variables de entorno.
# El plan gratuito de Render no tiene shell, así que se hace en el build.
python backend/manage.py crear_admin

# Carga los datos de demostración si CARGAR_DEMO=1 (idempotente).
if [ "${CARGAR_DEMO:-0}" = "1" ]; then
  python backend/manage.py cargar_demo
fi
