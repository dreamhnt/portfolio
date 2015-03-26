from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('letsstudy.views',
    # Examples:
    # url(r'^$', 'study.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'login_page'),
    url(r'^logout/', 'dologout'),

    url(r'^$', 'main_page'),
    url(r'^bbs/(?P<method>search)/$', 'main_page'),

    url(r'^test/', 'test_page'),
    url(r'^signup/', 'signup'),
    url(r'^login_check', 'login_check'),
    url(r'^write_page/', 'write_page'),
    url(r'^write', 'write'),

    url(r'^detail/(?P<num>\d+/$)', 'detail_page'),
    url(r'^comment/', 'comment'),
)
urlpatterns += static('media', document_root=settings.MEDIA_ROOT)
