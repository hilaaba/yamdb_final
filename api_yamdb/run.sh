#!/bin/bash
gunicorn api_yamdb.wsgi:application --bind 0:8000
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py loaddata fixtures.json