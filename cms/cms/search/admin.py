from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

from cms.search.models import SearchKeyword


class SearchKeywordInline(admin.StackedInline):
    model = SearchKeyword


class FlatPageAdminWithKeywords(FlatPageAdmin):
    inlines = [SearchKeywordInline]

# Whoa... that is a neat trick of registering and unregistering admin objects.
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdminWithKeywords)
