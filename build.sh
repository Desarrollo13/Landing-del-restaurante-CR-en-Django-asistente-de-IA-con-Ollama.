#!/usr/bin/env bash
# Script de build para Render: instala dependencias, recoge estáticos y migra.
set -o errexit

pip install -r requirements.txt

python backend/manage.py collectstatic --noinput
python backend/manage.py migrate --noinput
