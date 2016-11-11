from django.conf.urls import url
from .views import register, EventList, EventDetail, register_list

urlpatterns = [
    url(r'^$', EventList.as_view(), name='events'),
    url(r'^(?P<pk>\d+)/?$', EventDetail.as_view(), name='event'),
    url(r'^(?P<event_id>\d+)/register/?$', register, name='register'),
    url(r'^(?P<event_id>\d+)/registers/?$', register_list, name='registers'),
]
