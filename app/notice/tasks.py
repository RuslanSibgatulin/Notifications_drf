import json
import uuid
from datetime import datetime

from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import connection
from notice.models import Client, Mailing, Message, MsgStatus
from pydantic import BaseModel, SecretStr

from .sms_sender import SMSender, SMSMessage

logger = get_task_logger(__name__)


class Task(BaseModel):
    mailing_id: uuid.UUID
    client_id: uuid.UUID
    msg: str
    phone: SecretStr
    stop_client: datetime

    class Config:
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value()
        }


def get_current_recipients(since: datetime = None) -> list[Task]:
    st = since or datetime.utcnow().strftime("%Y-%m-%d %H:%M:00")
    query = """
    SELECT * FROM
    (
    SELECT
        nm.id mailing_id, nm.msg,
        nc.phone, nc.id client_id,
        nm.start_at AT TIME ZONE nc.tz start_client,
        nm.stop_at AT TIME ZONE nc.tz stop_client
    FROM notice_mailing nm
    JOIN notice_mailing_tag nmt ON nmt.mailing_id = nm.id
    JOIN notice_client_tag nct ON nct.tag_id = nmt.tag_id
    JOIN notice_client nc ON nct.client_id = nc.id
    ) ct
    WHERE ct.start_client BETWEEN '{0}' AND '{0}'::timestamp + interval '1 minute'
    """.format(st)
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        yield [Task.parse_obj(dict(zip(columns, row))) for row in cursor.fetchmany(100)]


@shared_task()
def send_notices():
    tasks_gen = get_current_recipients()

    while True:
        tasks = next(tasks_gen, None)
        if tasks is None:
            break

        for task in tasks:
            logger.info("Add task %s", task)

            send_sms_task.apply_async(
                args=[task.json()],
                expires=task.stop_client
            )


@shared_task()
def send_sms_task(data: str):
    task_data = Task.parse_obj(json.loads(data))
    logger.info("Exec task %s", task_data)
    msg = Message(mailing=Mailing(task_data.mailing_id), client=Client(task_data.client_id))
    msg.save()
    sms = SMSMessage(id=msg.id, phone=task_data.phone.get_secret_value(), text=task_data.msg)

    sender = SMSender(logger)
    res = sender.send(sms)

    if res:
        msg.status = MsgStatus.SUCCESS
    else:
        msg.status = MsgStatus.ERROR

    msg.save(update_fields=['status'])
