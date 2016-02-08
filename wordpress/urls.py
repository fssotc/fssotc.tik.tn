from __future__ import unicode_literals

from django.conf.urls import patterns, url
from .views import load_post_webhook


urlpatterns = [
    url(r"^load_post$", load_post_webhook, name="wp_rest_load_post_webhook"),
]
