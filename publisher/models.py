# django imports
from django.conf import settings
from django.db import models

# our own app imports
from utils import SSIContentResolver

class View(models.Model):
    page = models.CharField(
        max_length=128, 
        blank=True,
        null=True,
        # get choices on admin form
        choices=[(None, '---------'),],
        help_text='Select the page you want this view to render on.'
    )
    url = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text='Enter a specific url you want this page to render on. This overrides the page field.'
    )

class Publisher(models.Model):
    is_public = models.BooleanField(
        default=False, verbose_name="Public",
        help_text='Check to make this item visible to the public.'
    )

    targets =  models.ManyToManyField(
        'publisher.Widget', 
        blank=True, 
        help_text='Targets to which this content will be published.',
    )
    
    class Meta():
        abstract = True

class Widget(SSIContentResolver, models.Model):
    title = models.CharField(max_length=128)
    
    def __unicode__(self):
        return self.title

class Slot(models.Model):
    position = models.IntegerField()

    class Meta:
        abstract = True
        ordering = ('position',)

    def __unicode__(self):
        return "%s slot for %s" % (self.widget, self.layout)
