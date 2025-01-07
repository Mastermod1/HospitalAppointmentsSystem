#!/bin/sh

./scripts/wait_for_it.sh postgres:5432 --timeout=30 --strict -- echo "Database is up"

python manage.py makemigrations 
python manage.py migrate

python manage.py runserver 0.0.0.0:8000
