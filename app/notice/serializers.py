from rest_framework import serializers

from .models import Client, Mailing, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "phone", "provider_code", "tag", "tz"]


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = ["id", "start_at", "msg", "tag", "stop_at"]


class MailingStatsReportSerializer(serializers.Serializer):
    mailing = serializers.UUIDField()
    msg = serializers.StringRelatedField()
    start_at = serializers.DateTimeField()
    status = serializers.StringRelatedField()
    count = serializers.IntegerField()


class MailingDetailReportSerializer(serializers.Serializer):
    client = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    status = serializers.StringRelatedField()
    client_tz = serializers.StringRelatedField()
