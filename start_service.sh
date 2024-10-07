#!/bin/bash

echo "applying migrations"
python manage.py makemigrations
python manage.py migrate

# Start the Django server in the background
echo "Starting Django server..."
python manage.py runserver &

# Start the Celery worker in the background
echo "Starting Celery worker..."
celery -A catalyst_count worker --loglevel=info -P eventlet &

# Wait for all background processes to finish
wait
