from django.conf.urls import url, include

urlpatterns = [
        url(r'^', include('cf_stats.urls', namespace="cf_stats")),
]
