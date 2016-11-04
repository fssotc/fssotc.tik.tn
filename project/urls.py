from django.conf.urls import url, include
from django.contrib import admin
from website.views import index

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^$', index, name='index'),
    url(r'', include('website.urls'), name='website'),
    url(r'blog/', include('blog.urls'), name='blog'),
    url(r'inscription/', include('inscription.urls'), name='inscription'),
    url(r'^wordpress/', include('wordpress.urls')),
    url(r'^quiz/', include('quiz.urls')),
    url(r'', include('db.urls')),
]
