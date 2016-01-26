from django.conf.urls import url
from cf_stats import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contest/(?P<contest_id>\d+)$', views.contest_view, name='contest_view'),
]
