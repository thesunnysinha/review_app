#!/bin/bash

# Wait for the database to be ready
/app/entrypoint/wait-for-it.sh db:5432

python manage.py migrate

# Start the backend
python manage.py runserver