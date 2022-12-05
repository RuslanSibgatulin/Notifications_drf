from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Notice API",
        default_version='v1'
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('apidocs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('notice.urls', namespace="notice_api")),
]
