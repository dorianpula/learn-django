from django.conf.urls import patterns, include, url
from django.views.generic import YearArchiveView, MonthArchiveView, DayArchiveView, DateDetailView, ArchiveIndexView
from charleston.models import Entry

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from cms.settings import PROJECT_HOME

entry_info_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'publication_date',
}

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
    url(r'^tinymce/(?P<path>.*)$', 'django.views.static.serve', {'document_root':
                                                              '{}/templates/js/tinymce'.format(PROJECT_HOME)}),
    url(r'^search/$', 'cms.search.views.search'),

    url(r'^weblog/$', ArchiveIndexView.as_view(**entry_info_dict)),
    url(r'^weblog/(?P<year>\d{4})/$', YearArchiveView.as_view(**entry_info_dict)),
    url(r'^weblog/(?P<year>\d{4})/(?P<month>\w{3})/$', MonthArchiveView.as_view(**entry_info_dict)),
    url(r'^weblog/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', DayArchiveView.as_view(**entry_info_dict)),
    url(r'^weblog/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        DateDetailView.as_view(**entry_info_dict)),

    # Flatpages url.
    url(r'', include('django.contrib.flatpages.urls'))
)

