# python imports
import inspect, sys

# django imports
from django.conf import settings
from django.contrib import admin
from django.db import models

# our own app imports
from publisher.admin import ViewAdmin
from publisher.utils import SSIContentResolver

class View(models.Model):
    page = models.CharField(
        max_length=128, 
        blank=True,
        null=True,
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

# utility functions
def is_through_widget_field(field):
    """
    Determines if a field relates to the Widget model and if it has a through option set
    """
    from django.db.models.fields.related import ReverseManyRelatedObjectsDescriptor
    try:
        if field.__class__ == ReverseManyRelatedObjectsDescriptor:
            if Widget in field.field.rel.to.__mro__:
                return field.field.rel.through
    except AttributeError:
        return False
    return False

def create_through_models(cls):
    """
    Dynamically create 'through' classes and register for admin
    """
    if View in cls.__mro__ and cls != View:
        widget_through_fields = inspect.getmembers(cls, is_through_widget_field)
        inlines = []
        for widget_through_field in widget_through_fields:
            name = widget_through_field[0]
            field = widget_through_field[1].field
            through = field.rel.through
            new_model = type(
                through,
                (Slot,), 
                {
                    '__module__': cls.__module__,
                    'widget': models.ForeignKey(Widget, related_name='%s_slots' % name),
                    'layout': models.ForeignKey(cls, related_name='%s_slots' % name),
                }
            )
            inlines.append(type(
                "%sInline" % through,
                (admin.TabularInline,),
                {
                    'model': new_model,
                    'verbose_name': name.replace("_", " ").title(),
                    'verbose_name_plural': '%s' % name.replace("_", " ").title(),
                },
            ))
        cls_admin = type(
            "%sAdmin" % cls.__name__,
            (ViewAdmin,),
            {'inlines': inlines},
        )
    admin.site.register(cls, cls_admin)
