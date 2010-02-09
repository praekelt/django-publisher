from django import forms
from django.conf import settings
from django.contrib import admin

class PublisherAdmin(admin.ModelAdmin):
    list_display = ('is_public',)
    list_filter = ('is_public',)
    fieldsets = (
        ('Publishing', {
            'fields': ('is_public', 'targets',),
            'classes': ('collapse',),
        }),
    )

class ViewAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ViewAdminForm, self).__init__(*args, **kwargs)
        self.fields['page'].choices += self.get_page_choices()

    def get_page_choices(self):
        """
        generate page choices from url patterns
        """
        root_urlconf = __import__(settings.ROOT_URLCONF, globals(), locals(), ['urlpatterns',])
        page_choices = []
        for pattern in root_urlconf.urlpatterns:
            try:
                page_choices.append((pattern.name, pattern.name.title().replace('_', ' ')))
            except AttributeError:
                pass
        return page_choices

class ViewAdmin(admin.ModelAdmin):
    form = ViewAdminForm
