from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('oxontime.busses.views',
    (r'^$', 'home'), # Home page
    (r'^kml/$', 'kml'), # Home page

    (r'^admin/(.*)', admin.site.root),
)

