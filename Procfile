web: gunicorn sump.wsgi --log-file -
worker: celery -A sump worker
beat: celery -A sump beat -S django
