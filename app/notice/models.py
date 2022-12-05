import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class MsgStatus(models.TextChoices):
    SUCCESS = 'sended'
    ERROR = 'error'
    CANCELED = 'canceled'


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Mailing(UUIDMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_at = models.DateTimeField(_('start'))
    msg = models.CharField(_('message'), max_length=160)
    tag = models.CharField(_('tag'), max_length=200, blank=True)
    stop_at = models.DateTimeField(_('stop'))

    class Meta:
        db_table = "notice_mailing"
        verbose_name = _('Mailing')
        verbose_name_plural = _('Mailings')

    def __str__(self) -> str:
        return f"{self.id} {self.msg} [{self.start_at}-{self.stop_at}]"


class Client(UUIDMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = PhoneNumberField(
        _('phone'),
        region='RU',
        max_length=12,
        unique=True,
    )
    provider_code = models.IntegerField(
        _('provider code'),
        validators=[MinValueValidator(900), MaxValueValidator(999)]
    )
    tag = models.CharField(_('tag'), max_length=200, blank=True)
    tz = models.IntegerField(
        _('client time zone'),
        validators=[MinValueValidator(-10), MaxValueValidator(14)]
    )

    class Meta:
        db_table = "notice_client"
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')

    def __str__(self) -> str:
        return f"{self.id} {self.phone} [{self.tz}]"


class Message(UUIDMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('created'))
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
