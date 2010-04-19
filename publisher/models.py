from django.db import models

class Publisher(models.Model):
    title = models.CharField(max_length=64)

    def __unicode__(self):
        return "%s - %s" % (self._meta.verbose_name, self.title)

class Buzz(Publisher):
    # TODO: Add setup fields and methods to publish
    pass

class Facebook(Publisher):
    # TODO: Add setup fields and methods to publish
    class Meta:
        ordering = ('title',)
        verbose_name = 'Facebook'
        verbose_name_plural = 'Facebook'

class Mobile(Publisher):
    # TODO: Add setup fields and methods to publish
    pass

class Twitter(Publisher):
    # TODO: Add setup fields and methods to publish
    class Meta:
        ordering = ('title',)
        verbose_name = 'Twitter'
        verbose_name_plural = 'Twitter'

class SocialBookmark(Publisher):
    # TODO: Add setup fields and methods to publish
    pass

class Web(Publisher):
    # TODO: Add setup fields and methods to publish
    pass

#TODO: Add publishers for Mxit, Grid, Jil, Geo (Foursquare), Vlive, MTNPlay, V360, MyWeb.
