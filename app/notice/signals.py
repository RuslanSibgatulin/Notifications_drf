import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_save, sender='notice.Mailing')
def send_immediatlty(sender, instance, created, **kwargs):
    if created and instance.start_at and instance.stop_at:
        logger.info("Immediate task created %s", instance)
