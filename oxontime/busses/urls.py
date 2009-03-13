from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('oxontime.busses.views',
    (r'^$', 'home'), # Home page
    (r'^(?P<id>\d+)/$', 'respond'),
    (r'^(?P<id>\d+)/invite$', 'invite'),
    (r'^(?P<id>\d+)/results$', 'results'),
    (r'^(?P<id>\d+)/edit$', 'edit'),

    (r'^admin/(.*)', admin.site.root),
)

