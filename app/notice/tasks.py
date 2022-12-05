from datetime import datetime

from celery import shared_task
from celery.utils.log import get_task_logger
from notice.models import Mailing, Client

logger = get_task_logger(__name__)


@shared_task()
def send_notice():
    now_dt = datetime.now()
    mailinig = Mailing.objects.filter(
        start_at__date=now_dt.date(),
        start_at__hour=now_dt.time().hour,
        start_at__minute=now_dt.time().minute,
    )
    for task in mailinig:
        logger.info("Mailing task %s", task)
        clients = Client.objects.filter(tag=task.tag)
        for client in clients:
            send_sms_task.delay(
                client.phone,
                task.msg,
                task.stop_at
            )


@shared_task()
def send_sms_task(client_phone: str, message: str, stop_at: datetime):
    now_dt = datetime.now()
    if now_dt >= stop_at:
        logger.info("Sending overdue %s", client_phone)
        return

    logger.info("Sending SMS client %s", client_phone)
