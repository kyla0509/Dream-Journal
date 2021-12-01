# For development use (simple logging, etc):
/usr/bin/env flask run
# For production, add gunicorn to requirements and use: 
# gunicorn server:app -w 1 --log-file -
