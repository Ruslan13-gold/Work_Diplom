from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import path, include

from coolsite import settings
from dip.views import *
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dip.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_URL)

handler404 = pageNotFound
