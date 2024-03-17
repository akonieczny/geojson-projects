#!/bin/bash

gunicorn -k uvicorn.workers.UvicornWorker geojson_projects.app:app --workers 5 --bind 0.0.0.0:8000
