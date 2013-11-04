from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from cms.settings import PROJECT_HOME

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'cms.views.home', name='home'),
    # url(r'^cms/', include('cms.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # TinyMCE URLs...
    (r'^tinymce/(?P<path>.*)$', 'django.views.static.serve', {'document_root':
                                                              '{}/templates/js/tinymce'.format(PROJECT_HOME)}),


    # Flatpages url.
    url(r'^search/$', 'cms.search.views.search'),
    url(r'', include('django.contrib.flatpages.urls'))
)
