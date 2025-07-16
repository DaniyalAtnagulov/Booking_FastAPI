#!/bin/bash

# Запускаем миграции Alembic
alembic upgrade head

# Запускаем Gunicorn с Uvicorn-воркерами
gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000