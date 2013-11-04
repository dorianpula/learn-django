from django.db import models

from django.contrib.flatpages.models import FlatPage


class SearchKeyword(models.Model):
    """A search keyword to make searching flatpages simpler."""
    keyword = models.CharField(max_length=50)
    page = models.ForeignKey(FlatPage)

    def __unicode__(self):
        return self.keyword

