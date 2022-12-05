from rest_framework import generics

from .models import Client, Mailing, Tag
from .serializers import ClientSerializer, MailingSerializer, TagSerializer


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingList(generics.ListCreateAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MailingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer
