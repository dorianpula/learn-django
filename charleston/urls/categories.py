"""Categories!"""
from django.conf.urls import patterns
from django.views.generic import ListView

from charleston.models import Category

urlpatterns = patterns('charleston.views',
                      (r'^$', ListView.as_view(queryset=Category.objects.all())),
                      (r'^(?P<slug>[-\w]+)/$', 'charleston.views.category_detail'),)
