import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from timezone_field import TimeZoneField


class MsgStatus(models.TextChoices):
    SUCCESS = 'success'
    ERROR = 'error'
    CANCELED = 'canceled'


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Mailing(UUIDMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_at = models.DateTimeField(_('start at'))
    msg = models.CharField(_('message'), max_length=200)
    tag = models.CharField(_('tag'), max_length=50)
    stop_at = models.DateTimeField(_('stop at'))

    class Meta:
        db_table = "notice_mailing"
        verbose_name = _('Mailing')
        verbose_name_plural = _('Mailings')


class Client(UUIDMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(_('phone'), max_length=11)
    provider_code = models.IntegerField(_('provider code'))
    tag = models.CharField(_('tag'), max_length=50)
    tz = TimeZoneField()

    class Meta:
        db_table = "notice_client"
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')


class Message(UUIDMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('created at'))
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.PROTECT,
        verbose_name=_('mailing'),
    )
    cliend = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        verbose_name=_('client'),
    )
    status = models.CharField(
        _('status'), max_length=50,
        choices=MsgStatus.choices
    )

    class Meta:
        db_table = "notice_message"
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
