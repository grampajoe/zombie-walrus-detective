from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from comics.views import ComicRSS, ComicAtom

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^feed.rss$', ComicRSS(), name='rss'),
    url(r'^feed.atom$', ComicAtom(), name='atom'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'),
        name='about'),
    url(r'^omgsickbro/', include(admin.site.urls)),
)

urlpatterns += patterns('zombiewalrus.comics.views',
    url(r'^$', 'comic', name='home'),
    url(r'^contact/$', 'contact', name='contact'),
    url(r'^contact/thanks/$',
            TemplateView.as_view(template_name='contact_thanks.html'), 
            name='contact_thanks'),
    url(r'^archive/$', 'archive', name='archive'),
    url(r'^comments/(\d+)/approve/$', 'approve_comment',
            name='approve_comment'),
    url(r'^comments/(\d+)/delete/$', 'delete_comment',
            name='delete_comment'),
    url(r'^(\d+)/$', 'comic', {'lookup': 'pk'}, name='comic_pk'),
    # This MUST be the last item, or it might catch a lot of stuff
    url(r'^([\w-]+)/$', 'comic', {'lookup': 'slug'}, name='comic'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
