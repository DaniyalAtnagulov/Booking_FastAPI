from celery import Celery

from app.config import settings

celery = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=[
        "app.tasks.tasks",
        "app.tasks.scheduled"
]
)

#celery beat  (запускается в отдельном процессе) / папка scheduled.py

"""" продожить после докера там еще задание есть в 2.3 смотреть второе видео с началпа"""