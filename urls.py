from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from comics.views import ComicRSS, ComicAtom

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('zombiewalrus.comics.views',
    url(r'^$', 'comic', name='home'),
    url(r'^(\d+)/$', 'comic', name='comic'),
    url(r'^archive/$', 'archive', name='archive'),
)

urlpatterns += patterns('',
    url(r'^feed.rss$', ComicRSS(), name='rss'),
    url(r'^feed.atom$', ComicAtom(), name='atom'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'),
        name='about'),
    url(r'^omgsickbro/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
