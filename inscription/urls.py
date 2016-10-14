from django.conf.urls import url, include
from .views import inscription, success

app_name = 'inscription'
urlpatterns = [
    url(r'^$', inscription, name='inscription'),
    # url(r'^$', InscriptionView.as_view(), name='inscription'),
    url(r'success/?', success, name='sucess'),
]
