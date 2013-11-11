from datetime import datetime

from django.core.urlresolvers import reverse, reverse_lazy
from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.utils.encoding import smart_str

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

    def live_entry_set(self):
        return self.entry_set.filter(status=Entry.LIVE_STATUS)


class LiveEntryManager(models.Manager):
    """Gets only the entries that have a live status."""

    def get_queryset(self):
        return super(LiveEntryManager, self).get_queryset().filter(status=self.model.LIVE_STATUS)


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

    # Hook in the nice manager we've written above.
    live = LiveEntryManager()
    objects = models.Manager()

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
        """Gets the absolute URL for an entry."""
        return reverse("charleston_entry_detail",
                       kwargs={"year": self.pub_date.strftime("%Y"),
                               "month": self.pub_date.strftime("%b").lower(),
                               "day": self.pub_date.strftime("%d"),
                               "slug": self.slug})

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
    slug = models.SlugField(unique_for_date='pub_date')

    tags = TagField()

    # Allow for commenting and posting to external sites
    enable_comments = models.BooleanField(default=True)
    post_elsewhere = models.BooleanField(default=True)

    # Extra link metadata
    via_name = models.CharField('Via', max_length=250, blank=True,
                                help_text='The name of the person whose site you spotted the link on.  Optional.')
    via_url = models.URLField('Via URL', blank=True,
                              help_text='The URL of the site where you spotted the link. Optional.')

    class Meta:
        ordering = ['-pub_date']

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Saves a link.  Updates the rendered description HTML and make sure the link gets posted elsewhere.
        """

        if self.description:
            self.description_html = markdown(self.description)

        # Update delicious
        if not self.id and self.post_elsewhere:
            import pydelicious
            pydelicious.add(settings.DELICIOUS_USER, settings.DELICIOUS_PASSWORD,
                            smart_str(self.url), smart_str(self.title), smart_str(self.tags))

        super(Link, self).save(force_insert=force_insert, force_update=force_update, using=using,
                               update_fields=update_fields)

    def get_absolute_url(self):
        """Gets the absolute URL of the link."""
        return reverse("charleston_link_detail",
                       kwargs={"year": self.pub_date.strftime("%Y"),
                               "month": self.pub_date.strftime("%b").lower(),
                               "day": self.pub_date.strftime("%d"),
                               "slug": self.slug})


