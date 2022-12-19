import logging
from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from notice.tasks import immediate_notices
from pytz import utc

logger = logging.getLogger(__name__)


@receiver(post_save, sender="notice.Mailing")
def on_post_save_mailing(sender, instance, created, **kwargs):
    if created:
        logger.debug("Mailing created <%s>", instance)
        if instance.start_at < datetime.now(utc):
            logger.info("Immediate sending mailing <%s>", instance)
            immediate_notices.apply_async(
                args=[instance.id]
            )
