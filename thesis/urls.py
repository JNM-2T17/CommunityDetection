from django.conf.urls import url
from . import views

app_name = 'thesis'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'vis.html', views.vis, name='vis'),
    url(r'run.html', views.run, name='run_algo'),
]