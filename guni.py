"""gunicorn WSGI server configuration."""
from multiprocessing import cpu_count
from os import environ


def max_workers():
    return cpu_count()


bind = '0.0.0.0:' + environ.get('PORT', '8000')
loglevel=debug
#max_requests = 1000
worker_class = 'socketio.sgunicorn.GeventSocketIOWorker'
workers = max_workers()


#gunicorn --debug --bind 0.0.0.0:8000 --worker-class socketio.sgunicorn.GeventSocketIOWorker app:app -D
