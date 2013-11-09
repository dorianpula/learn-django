from django.conf.urls import patterns, url
from django.views.generic import YearArchiveView, MonthArchiveView, DayArchiveView, ArchiveIndexView, DateDetailView
from django.views.generic import ListView, DetailView

from charleston.models import Category, Entry, Link
from tagging.models import Tag

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',

    # URLS for the blog posts.
    url(r'^$',
        ArchiveIndexView.as_view(queryset=Entry.objects.all(), date_field='pub_date')),
    url(r'^(?P<year>\d{4})/$',
        YearArchiveView.as_view(queryset=Entry.objects.all(), date_field='pub_date')),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        MonthArchiveView.as_view(queryset=Entry.objects.all(), date_field='pub_date')),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
        DayArchiveView.as_view(queryset=Entry.objects.all(), date_field='pub_date')),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        DateDetailView.as_view(queryset=Entry.objects.all(), date_field='pub_date'),
        name="charleston_entry_detail"),

    # URLs for the links.
    url(r'links/^$',
        ArchiveIndexView.as_view(queryset=Link.objects.all(), date_field='pub_date')),
    url(r'^links/(?P<year>\d{4})/$',
        YearArchiveView.as_view(queryset=Link.objects.all(), date_field='pub_date')),
    url(r'^links/(?P<year>\d{4})/(?P<month>\w{3})/$',
        MonthArchiveView.as_view(queryset=Link.objects.all(), date_field='pub_date')),
    url(r'^links/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
        DayArchiveView.as_view(queryset=Link.objects.all(), date_field='pub_date')),
    url(r'^links/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        DateDetailView.as_view(queryset=Link.objects.all(), date_field='pub_date'),
        name="charleston_link_detail")
)

urlpatterns += patterns('charleston.views',
                        (r'^categories/$', ListView.as_view(queryset=Category.objects.all())),
                        (r'^categories/(?P<slug>[-\w]+)/$', 'category_detail'),)

urlpatterns += patterns('',
                        (r'^tags/$', ListView.as_view(queryset=Tag.objects.all())),
                        (r'^tags/entries/(?P<tag>[-\w]+)/$', 'tagging.views.tagged_object_list',
                         {'queryset_or_model': Entry, 'template_name': 'charleston/entries_by_tag.html'}),
                        (r'^tags/links/(?P<tag>[-\w]+)/$', 'tagging.views.tagged_object_list',
                         {'queryset_or_model': Link, 'template_name': 'charleston/links_by_tag.html'}),
)

