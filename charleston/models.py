from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

from tagging.fields import TagField
from markdown import markdown


class Category(models.Model):
    """Categories of stories."""
    title = models.CharField(max_length=250, help_text="Maximum 250 characters.")

    slug = models.SlugField(unique=True,
                            help_text="Suggested value automatically generated from title. Must be unique.")

    description = models.TextField()

    class Meta:
        ordering = ['title']
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/categories/{}/".format(self.slug)


class Entry(models.Model):
    """Entry or blog post model."""

    title = models.CharField(max_length=250)
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    pub_date = models.DateTimeField(default=datetime.now)

    slug = models.SlugField(unique_for_date='pub_date')

    # Authors, comments and the like.
    author = models.ForeignKey(User)
    enable_comments = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    # Status to enable different types of entries
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)

    # Now for the categories and tags
    categories = models.ManyToManyField(Category)
    tags = TagField()

    # Separate HTML rendered entries to allow for fast loading.  (Space vs. processor tradeoff)
    excerpt_html = models.TextField(editable=False, blank=True)
    body_html = models.TextField(editable=False, blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        """Recreate the HTML from Markdown before saving the entry."""
        self.body_html = markdown(self.body)
        if self.excerpt:
            self.excerpt_html = markdown(self.excerpt)
        super(Entry, self).save(force_insert, force_update, using, update_fields)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ('charleston_entry_detail', (),
                {"year": self.pub_date.strftime("%Y"),
                 "month": self.pub_date.strftime("%b").lower(),
                 "date": self.pub_date.strftime("%d"),
                 "slug": self.slug})

    get_absolute_url = models.permalink(get_absolute_url)

    class Meta:
        verbose_name_plural = "Entries"
        ordering = ["-pub_date"]


class Link(models.Model):
    """Links model hyperlinks to various URLs both external and internal."""

    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    description_html = models.TextField(blank=True)
    url = models.URLField(unique=True)

    posted_by = models.ForeignKey(User)
    pub_date = models.DateTimeField(default=datetime.now)

