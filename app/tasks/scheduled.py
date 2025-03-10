from app.tasks.celery_app import celery


@celery.task(name="periodic_task")
def periodic_task():  #периодическая задача
    print(12345)   
    
"""" продожить после докера там еще задание есть в 2.3 смотреть второе видео с началпа"""