#!/bin/bash
gunicorn api_yamdb.wsgi:application --bind 0:8000