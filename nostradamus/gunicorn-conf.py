import multiprocessing

# gunicorn workers configuration
workers = multiprocessing.cpu_count() * 2 + 1
max_requests = 2
timeout = 86400
preload_app = True
keepalive = 200
enable_stdio_inheritance = True
bind = "0.0.0.0:8000"
worker_class = "uvicorn.workers.UvicornH11Worker"
accesslog = "-"
errorlog = "-"
loglevel = "debug"
