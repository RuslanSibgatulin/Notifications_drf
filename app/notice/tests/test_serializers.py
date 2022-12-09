from django.test import TestCase
from notice.serializers import (ClientSerializer,
                                MailingDetailReportSerializer,
                                MailingSerializer,
                                MailingStatsReportSerializer, TagSerializer)


class SerializersTestClass(TestCase):

    def test_TagSerializer(self):
        serializer = TagSerializer()
        self.assertEqual(
            list(serializer.get_fields()), ['id', 'name']
        )

    def test_ClientSerializer(self):
        serializer = ClientSerializer()
        self.assertEqual(
            list(serializer.get_fields()), ['id', 'phone', 'provider_code', 'tag', 'tz']
        )

    def test_MailingSerializer(self):
        serializer = MailingSerializer()
        self.assertEqual(
            list(serializer.get_fields()), ['id', 'start_at', 'msg', 'tag', 'stop_at']
        )

    def test_MailingDetailReportSerializer(self):
        serializer = MailingDetailReportSerializer()
        self.assertEqual(
            list(serializer.get_fields()), ['client', 'created_at', 'status', 'client_tz']
        )

    def test_MailingStatsReportSerializer(self):
        serializer = MailingStatsReportSerializer()
        self.assertEqual(
            list(serializer.get_fields()), ['mailing', 'msg', 'start_at', 'status', 'count']
        )
