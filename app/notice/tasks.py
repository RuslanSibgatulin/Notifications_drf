import json
from typing import Generator

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from notice.db.models import Task
from notice.db.pg_utils import pgTasks
from notice.models import Client, Mailing, Message, MsgStatus
from notice.senders.sms_sender import SMSender, SMSMessage

logger = get_task_logger(__name__)
tasks_storage = pgTasks()


def add_sending_tasks(tasks_gen: Generator):
    """Adds a batch of tasks to the queue

    Args:
        tasks_gen (Generator): List of instances Task
    """
    while (tasks := next(tasks_gen, None)):
        for task in tasks:
            logger.info("Add task %s", task)

            send_sms_task.apply_async(
                args=[task.json()],
                expires=task.stop_client
            )


@shared_task()
def scheduled_notices():
    """Scheduled task for CELERY_BEAT_SCHEDULE. Search for clients to send at the current time.
    """
    add_sending_tasks(
        tasks_storage.get_tasks_by_time(interval=settings.CELERY_SCHEDULE_INTERVAL)
    )


@shared_task()
def immediate_notices(mailing_id: str):
    """Immediate task. Search for clients to send by a given mailing.
    """
    add_sending_tasks(
        tasks_storage.get_immediate_mailing_tasks(mailing_id)
    )


@shared_task()
def send_sms_task(task_str_data: str):
    """Creates the task to send single message for client.
    Creates the log message with sending status.

    Args:
        task_str_data (str): JSON string with task data
    """
    task_data = Task.parse_obj(json.loads(task_str_data))
    logger.info("Exec task %s", task_data)
    msg = Message(mailing=Mailing(task_data.mailing_id), client=Client(task_data.client_id))
    msg.save()
    sms = SMSMessage(
        id=msg.id,
        phone=task_data.phone.get_secret_value(),
        text=task_data.msg
    )

    sender = SMSender(logger)
    res = sender.send(sms)

    if res:
        msg.status = MsgStatus.SUCCESS
    else:
        msg.status = MsgStatus.ERROR

    msg.save(update_fields=["status"])
