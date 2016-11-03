from django.conf.urls import url
from .views import email

urlpatterns = [
    url(r'^send_mail$', email, name='send_mail'),
]
