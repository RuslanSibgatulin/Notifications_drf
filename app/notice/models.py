import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class MsgStatus(models.TextChoices):
    CREATED = "created"
    SUCCESS = "sended"
    ERROR = "error"
    CANCELLED = "cancelled"


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Tag(models.Model):
    name = models.CharField(_("tag name"), max_length=50)

    def __str__(self) -> str:
        return f"{self.name}"


class Mailing(UUIDMixin):
    start_at = models.DateTimeField(_("start"))
    msg = models.CharField(_("message"), max_length=160)
    tag = models.ManyToManyField(Tag)
    stop_at = models.DateTimeField(_("stop"))

    class Meta:
        db_table = "notice_mailing"
        verbose_name = _("Mailing")
        verbose_name_plural = _("Mailings")

    def __str__(self) -> str:
        return f"{self.msg} [{self.start_at}]"


class Client(UUIDMixin):
    phone = PhoneNumberField(
        _("phone"),
        region="RU",
        max_length=12,
        unique=True,
    )
    provider_code = models.IntegerField(
        _("provider code"),
        validators=[MinValueValidator(900), MaxValueValidator(999)]
    )
    tag = models.ManyToManyField(Tag)
    tz = models.CharField(
        _("client time zone"),
        max_length=50,
        default="UTC+03:00"
    )

    class Meta:
        db_table = "notice_client"
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

    def __str__(self) -> str:
        return f"{self.phone} [{self.tz}]"


class Message(models.Model):
    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.PROTECT,
        verbose_name=_("mailing"),
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        verbose_name=_("client"),
    )
    status = models.CharField(
        _("status"),
        max_length=50,
        choices=MsgStatus.choices,
        default=MsgStatus.CREATED
    )

    class Meta:
        db_table = "notice_message"
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
