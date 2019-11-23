from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from welcome.views import index, health

urlpatterns = [
    path('health', health),
    path('admin/', admin.site.urls),
    path('', include('auctionapp.urls')),
]
