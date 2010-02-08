from django.db import models

class Publisher(models.Model):
    is_public = models.BooleanField(
        default=False, verbose_name="Public",
        help_text='Check to make this item visible to the public.'
    )
    
    class Meta():
        abstract = True
