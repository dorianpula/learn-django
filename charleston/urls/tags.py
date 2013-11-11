"""URLs for the tags."""
from django.views.generic import ListView
from django.conf.urls import patterns, url

from charleston.models import Entry, Link
from tagging.models import Tag


urlpatterns = patterns('',
                       (r'^$', ListView.as_view(queryset=Tag.objects.all())),
                       (r'^entries/(?P<tag>[-\w]+)/$', 'tagging.views.tagged_object_list',
                        {'queryset_or_model': Entry.live.all(), 'template_name': 'charleston/entries_by_tag.html'}),
                       (r'^links/(?P<tag>[-\w]+)/$', 'tagging.views.tagged_object_list',
                        {'queryset_or_model': Link, 'template_name': 'charleston/links_by_tag.html'}),)
