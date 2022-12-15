import logging
from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import immediate_notices

logger = logging.getLogger(__name__)


@receiver(post_save, sender='notice.Mailing')
def send_immediately(sender, instance, created, **kwargs):
    if created and instance.start_at < datetime.utcnow():
        logger.info("Immediate task created %s", instance)
        immediate_notices.apply_async(
            args=[instance.id]
        )
