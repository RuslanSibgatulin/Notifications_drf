from rest_framework import serializers
from .models import Client, Mailing


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'phone', 'provider_code', 'tag', 'tz']


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = ['id', 'start_at', 'msg', 'tag', 'stop_at']
