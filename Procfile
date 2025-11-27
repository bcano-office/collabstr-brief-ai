web: python manage.py migrate && python manage.py collectstatic --noinput && python -m gunicorn collabstr_ai.wsgi:application --bind 0.0.0.0:$PORT

