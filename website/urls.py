from django.conf.urls import url, include
from .views import MemberList, wpad

app_name = 'website'
urlpatterns = [
    url(r'members/?$', MemberList.as_view(), name='members'),
    url(r'wpad.dat$', wpad, name='wpad'),
]
