#!/bin/bash

# Останавливаем выполнение при ошибке
set -e

# Применяем миграции
echo "🔁 Running migrations..."
python manage.py migrate

# Собираем статику
echo "🎯 Collecting static files..."
python manage.py collectstatic --noinput

# Запускаем Gunicorn
echo "🚀 Starting Gunicorn..."
exec gunicorn leehaaatch.wsgi:application --bind 0.0.0.0:8000
