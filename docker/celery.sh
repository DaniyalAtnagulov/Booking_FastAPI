#!/bin/bash

if [[ "${1}" == "celery" ]]; then
    celery --app=app.tasks.celery_app:celery worker -l INFO
elif [[ "${1}" == "celery_beat" ]]; then
    celery --app=app.tasks.celery_app:celery worker -l INFO -B
elif [[ "${1}" == "flower" ]]; then
    celery --app=app.tasks.celery_app:celery flower
else
    echo "Unknown command: $1"
    echo "Usage: $0 {celery|celery_beat|flower}"
fi