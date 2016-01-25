from django.conf.urls import url
from cf_stats import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
