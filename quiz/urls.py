from django.conf.urls import url

from .views import quiz

urlpatterns = [
    url(r'^(?P<quiz_pk>\d+)/?$', quiz, name='quiz'),
    url(r'^(?P<quiz_title>\w+)/?$', quiz),
    url(r'^(?P<quiz_pk>\d+)/(?P<member_pk>\d+)/?$', quiz),
    url(r'^(?P<quiz_title>\w+)/(?P<member_pk>\d+)/?$', quiz),
    url(r'^(?P<quiz_title>\w+)/(?P<member_email>\S+@\S+)$', quiz,
        name='submission'),
]
