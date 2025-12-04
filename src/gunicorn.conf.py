# Listening only on loopback to avoid accidental direct exposure of the application server without a reverse proxy
bind = '127.0.0.1:5001'

# Just log to stdout for now
errorlog = '-'
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'