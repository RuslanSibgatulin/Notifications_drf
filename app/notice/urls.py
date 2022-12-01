from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ClientDetail, ClientList

app_name = 'notice_api'

urlpatterns = [
    path('clients/', ClientList.as_view()),
    path('clients/<uuid:pk>/', ClientDetail.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
