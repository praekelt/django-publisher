from django.contrib import admin

from publisher.models import Buzz, Facebook, Mobile, SocialBookmark, Twitter, \
        Web

admin.site.register(Buzz)
admin.site.register(Facebook)
admin.site.register(Mobile)
admin.site.register(SocialBookmark)
admin.site.register(Twitter)
admin.site.register(Web)
