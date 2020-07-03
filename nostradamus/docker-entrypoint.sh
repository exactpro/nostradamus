#!/bin/bash

echo "Applying database migrations"

python manage.py migrate
