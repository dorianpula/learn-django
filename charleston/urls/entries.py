"""URLs for the blog posts."""

from django.conf.urls import patterns, url
from django.views.generic import YearArchiveView, MonthArchiveView, DayArchiveView, ArchiveIndexView, DateDetailView

from charleston.models import Entry

urlpatterns = patterns(
    '',

    url(r'^$',
        ArchiveIndexView.as_view(queryset=Entry.live.all(), date_field='pub_date')),
    url(r'^(?P<year>\d{4})/$',
        YearArchiveView.as_view(queryset=Entry.live.all(), date_field='pub_date')),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        MonthArchiveView.as_view(queryset=Entry.live.all(), date_field='pub_date')),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
        DayArchiveView.as_view(queryset=Entry.live.all(), date_field='pub_date')),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        DateDetailView.as_view(queryset=Entry.live.all(), date_field='pub_date'),
        name="charleston.views.charleston_entry_detail"),
)
