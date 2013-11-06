from django.conf.urls import patterns, url
from django.views.generic import YearArchiveView, MonthArchiveView, DayArchiveView, DateDetailView, ArchiveIndexView
from charleston.models import Entry

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


entry_info_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'pub_date',
}

urlpatterns = patterns(
    '',

    url(r'^$', ArchiveIndexView.as_view(template_name="charleston/entry_archive", **entry_info_dict)),
    url(r'^(?P<year>\d{4})/$', YearArchiveView.as_view(template_name="charleston_entry_archive_year", **entry_info_dict)),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$', MonthArchiveView.as_view(**entry_info_dict)),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', DayArchiveView.as_view(**entry_info_dict)),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        DateDetailView.as_view(template_name="charleston_entry_detail", **entry_info_dict)),
)
