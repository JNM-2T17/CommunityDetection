from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^thesis/', include('thesis.urls')),
    url(r'^admin/', admin.site.urls),
]
