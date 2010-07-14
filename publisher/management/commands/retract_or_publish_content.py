from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from content.models import ModelBase

class Command(BaseCommand):
    def handle(self, *app_labels, **options):
        now = datetime.now()

        # publish those items that have a publish_on datetime set in the past
        to_publish = ModelBase.objects.filter(publish_on__lte=now)
        for obj in to_publish:
            obj.is_public = True
            obj.publish_on = None
            obj.save()
        
        # retract those items that have a retract_on datetime set in the past
        to_retract = ModelBase.objects.filter(retract_on__lte=now)
        for obj in to_retract:
            obj.is_public = False
            obj.retract_on = None
            obj.save()
