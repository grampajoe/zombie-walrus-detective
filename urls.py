from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('zombiewalrus.comics.views',
    url(r'^$', 'comic', name='home'),
    url(r'^comic/(\d+)/$', 'comic', name='comic'),
    url(r'^archive/$', 'archive', name='archive'),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
