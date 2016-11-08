from django.conf.urls import url
from .views import register

urlpatterns = [
    url(r'^(?P<event_id>\d+)/register/?$', register),
]
