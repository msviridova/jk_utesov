from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static


urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + [
    path('', admin.site.urls),
    path('admin_tools/', include('admin_tools.urls')),
]
