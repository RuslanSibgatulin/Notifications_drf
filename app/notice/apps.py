from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NoticeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notice'
    verbose_name = _('notice')
