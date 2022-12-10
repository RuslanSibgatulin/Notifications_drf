from rest_framework import generics

from .models import Client, Mailing, Tag
from .report import mailing_detail_report, mailing_stats_report
from .serializers import (ClientSerializer, MailingDetailReportSerializer,
                          MailingSerializer, MailingStatsReportSerializer,
                          TagSerializer)


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all().order_by("name")
    serializer_class = TagSerializer


class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all().order_by("provider_code")
    serializer_class = ClientSerializer


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingList(generics.ListCreateAPIView):
    queryset = Mailing.objects.all().order_by("start_at")
    serializer_class = MailingSerializer


class MailingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MailingStatsReportAPIView(generics.ListAPIView):
    queryset = mailing_stats_report()
    serializer_class = MailingStatsReportSerializer


class MailingDetailReportAPIView(generics.ListAPIView):
    serializer_class = MailingDetailReportSerializer

    def get_queryset(self):
        return mailing_detail_report(self.kwargs["pk"])
