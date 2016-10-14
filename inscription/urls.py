from django.conf.urls import url, include
from .views import InscriptionView, success

app_name = 'inscription'
urlpatterns = [
    url(r'^$', InscriptionView.as_view(), name='inscription'),
    url(r'success/?', success, name='sucess'),
]
