""" Gunigorn production cinfiguration file """

import multiprocessing


# user running the application
user = "root"

wsgi_app = "backend.wsgi:application"

workers = multiprocessing.cpu_count() * 2 + 1

bind = "0.0.0.0:8000"

accesslog = "/backend/logs/backend-access.log"
errorlog = "/backend/logs/backend-error.log"

capture_output = True
