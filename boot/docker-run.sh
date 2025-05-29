
#!/bin/bash

ARG PROJ_NAME="cfehome"

source /opt/venv/bin/activate

cd /code

python manage.py sendtestemail --admins
python manage.py migrate --no-input
python manage.py auto_admin

export RUNTIME_PORT=8080

# add our static files to the container itself on run
# python manage.py collectstatic --no-input 
gunicorn ${PROJ_NAME}.wsgi:application --bind 0.0.0.0:$RUNTIME_PORT