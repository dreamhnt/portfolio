from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from blogapp.views import *
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', main_page),
    url(r'^login/$', login_page),
    url(r'^logout/$', logout_page),
    url(r'^check/$', login_check),
    url(r'^register/$', register_page),

    url(r'^music_page/$', music_page),
    url(r'^search/$', search_page),
    url(r'^musicbox/$', musicbox),

    url(r'^profile/$', profile),
    url(r'^notice_page/$', notice_page),

    url(r'^gallery_page/$', gallery_page),
    url(r'^gallery/$', gallery),
    url(r'^picture_up/$', picture_up),
    url(r'^gallery/like/$',like_view),

    url(r'^one_page/$', Oneblog),
    url(r'^blog/submit/$', submit),
    url(r'^blog/(?P<article_id>\d+)/remove/$', remove),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))

