from datetime import datetime
from typing import Generator, List

from django.db import connection

from .models import Task


class pgTasks:
    def __init__(self, limit: int = 100) -> None:
        self.limit = limit

    def exec_query(self, query: str) -> Generator[List[Task], None, None]:
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            yield [
                Task.parse_obj(dict(zip(columns, row))) for row in cursor.fetchmany(self.limit)
            ]

    def get_immediate_mailing_tasks(self, mailing_id: str) -> Generator[List[Task], None, None]:
        query = """
        SELECT * FROM
        (
            SELECT
                nm.id mailing_id, nm.msg, nc.phone, nc.id client_id,
                datetime(nm.start_at, substr(nc.tz, 4, 6)) start_client,
                datetime(nm.stop_at, substr(nc.tz, 4, 6)) stop_client
            FROM notice_mailing nm
            JOIN notice_mailing_tag nmt ON nmt.mailing_id = nm.id
            JOIN notice_client_tag nct ON nct.tag_id = nmt.tag_id
            JOIN notice_client nc ON nct.client_id = nc.id
            WHERE mailing_id={0}
        ) ct
        WHERE ct.start_client >= datetime('now') AND ct.stop_client > datetime('now')
        """.format(mailing_id)

        return self.exec_query(query)

    def get_tasks_by_time(self, since: datetime = None, interval: int = 1) -> Generator[List[Task], None, None]:
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
            WHERE ct.start_client BETWEEN "{0}" AND "{0}"::timestamp + interval "{1} minute"
        """.format(st, interval)

        return self.exec_query(query)
