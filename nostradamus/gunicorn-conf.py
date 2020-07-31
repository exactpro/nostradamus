import multiprocessing

# gunicorn workers configuration
workers = multiprocessing.cpu_count() * 2 + 1
graceful_timeout = 86400
timeout = 86400
preload_app = True
keepalive = 200
enable_stdio_inheritance = True
