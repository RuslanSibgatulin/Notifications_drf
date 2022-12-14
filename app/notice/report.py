from django.db.models import Count, F

from .models import Message


def mailing_stats_report():
    return Message.objects.values(
        "mailing",
        "status"
    ).annotate(
        msg=F("mailing__msg"),
        start_at=F("mailing__start_at"),
        count=Count("status")
    )


def mailing_detail_report(mailing_id: str):
    return Message.objects.filter(
        mailing__pk=mailing_id
    ).values(
        "client",
        "created_at",
        "status"
    ).annotate(
        client_tz=F("client__tz"),
    )
