cd /app
sudo chown -R app:app /app
pipenv run python manage.py migrate
pipenv run gunicorn --bind :8000 --workers 3 --reload gmop.wsgi --daemon

