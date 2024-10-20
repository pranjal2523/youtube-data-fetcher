# gunicorn.conf.py

bind = "0.0.0.0:8000"
workers = 3  # Number of worker processes for handling requests
threads = 2  # Number of threads per worker
timeout = 3000  # Request timeout in seconds
