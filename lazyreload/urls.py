from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='LazyApp API',
        default_version='v1',
        description='API for Job and Flat Applications',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='lazyapp@mail.de'),
        lincense=openapi.License(name='MIT License')
    ),
    public=True,
    permission_classes=[],
    authentication_classes=[]
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.users.urls", namespace="users")),
    path("", include("apps.job_applications.urls", namespace="job_applications")),
    path("", include("apps.flat_applications.urls", namespace="flat_applications")),
    # swagger
    path("openapi/", schema_view.without_ui(cache_timeout=0)),
    path("swagger/", schema_view.with_ui("swagger",cache_timeout=0),name="schema-swagger-ui"),
    path("redoc/",schema_view.with_ui("redoc",cache_timeout=0),name="schema-redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
