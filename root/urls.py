from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

from root import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.urls')),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path('api/v1/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
