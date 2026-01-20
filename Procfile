release: python3 manage.py migrate --noinput
web: gunicorn cookie.wsgi:application --bind 0.0.0.0:${PORT} --access-logfile -
