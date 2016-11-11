from django.conf.urls import url
from .views import register, EventList, EventDetail, RegisterList

urlpatterns = [
    url(r'^$', EventList.as_view(), name='events'),
    url(r'^(?P<pk>\d+)/?$', EventDetail.as_view(), name='event'),
    url(r'^(?P<event_id>\d+)/register/?$', register, name='register'),
    url(r'^(?P<event_id>\d+)/registers/?$', RegisterList.as_view(),
        name='registers'),
]
