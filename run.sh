#!/bin/bash

echo "run makemigrations"
python3 manage.py makemigrations
sleep 5
echo "run migrate"
python3 manage.py migrate

echo "run server"
python3 manage.py runserver 0.0.0.0:8000
