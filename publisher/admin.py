from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin


class PublisherAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PublisherAdminForm, self).__init__(*args, **kwargs)
        self.fields['targets'].choices = self.get_target_choices()

    def get_target_choices(self):
        from publisher.models import Widget
        app_model_label = '.'.join((self._meta.model._meta.app_label, self._meta.model._meta.object_name))
        widgets = Widget.objects.all()
        choices = []
        for widget in widgets:
            if app_model_label in widget.as_leaf_class().restricted_to:
                choices.append((widget.id, str(widget)))
        return choices

class PublisherAdmin(admin.ModelAdmin):
    form = PublisherAdminForm
    list_display = ('is_public',)
    list_filter = ('is_public',)
    fieldsets = (
        ('Publishing', {
            'fields': ('is_public', 'targets',),
            'classes': ('collapse',),
        }),
    )

class PublisherInlineModelAdmin(InlineModelAdmin):
    form = PublisherAdminForm

class PublisherStackedInline(PublisherInlineModelAdmin, admin.StackedInline):
    pass

class PublisherTabularInline(PublisherInlineModelAdmin, admin.TabularInline):
    pass

class ViewAdminForm(forms.ModelForm):
    page = forms.ChoiceField()
    
    def __init__(self, *args, **kwargs):
        super(ViewAdminForm, self).__init__(*args, **kwargs)
        self.fields['page'].choices = self.get_page_choices()

    def get_page_choices(self):
        """
        generate page choices from url patterns
        """
        root_urlconf = __import__(settings.ROOT_URLCONF, globals(), locals(), ['urlpatterns',])
        page_choices = [(None, '---------'),]
        for pattern in root_urlconf.urlpatterns:
            try:
                page_choices.append((pattern.name, pattern.name.title().replace('_', ' ')))
            except AttributeError:
                pass
        return page_choices
    
class ViewAdmin(admin.ModelAdmin):
    form = ViewAdminForm
