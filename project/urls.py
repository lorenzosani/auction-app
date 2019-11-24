from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static

from welcome.views import index, health

urlpatterns = [
    path('health', health),
    path('admin/', admin.site.urls),
    path('', include('auctionapp.urls')),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)