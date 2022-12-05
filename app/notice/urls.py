from django.urls import path

from .views import ClientDetail, ClientList, MailingDetail, MailingList

app_name = 'notice_api'

urlpatterns = [
    path('clients/', ClientList.as_view()),
    path('clients/<uuid:pk>/', ClientDetail.as_view()),
    path('mailings/', MailingList.as_view()),
    path('mailings/<uuid:pk>/', MailingDetail.as_view()),
]
