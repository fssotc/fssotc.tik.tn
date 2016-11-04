from django.conf.urls import url

from .views import python_quiz

urlpatterns = [
    url(r'^python$', python_quiz),
]
