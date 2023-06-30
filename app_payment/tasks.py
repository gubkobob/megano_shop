from time import sleep

from celery import shared_task

@shared_task
def logika():
    """Sends an email when the feedback form has been submitted."""
    glist = [1, 2, 3, 4, 5]
    for id in glist:
        print(id)
    sleep(10)  # Simulate expensive operation(s) that freeze Django
