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
            'fields': ('is_public', 'publish_on', 'retract_on', 'targets',),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        We are dis/connecting targets here because there is no other sane place to do it.
        Signlas and model saves just don't work consistently.
        """
        remove_targets = False
        try:
            form_targets = form.cleaned_data['targets']
            remove_targets = True
        except KeyError:
            form_targets = []

        super(PublisherAdmin, self).save_model(request, obj, form, change)
        
        if not obj.ignore_targets:

            # get exsiting targets from object
            all_targets = [target for target in obj.targets.all()]
            
            # determine which targets to add. a target should be added if it's in the form's 
            # targets but is not in the existing objects stored targets.
            add_targets = []
            for target in form_targets:
                if target not in all_targets:
                    add_targets.append(target)
           
            # connect add targets
            for target in add_targets:
                target.as_leaf_class().connect_content(obj)

            # determine which targets to remove. a target should be removed if it's in the 
            # existing objects stored targets but not in the form's targets.  don't remove anything
            # if we were unable to collect form targets.
            if remove_targets:
                remove_targets = []
                for target in all_targets:
                    if target not in form_targets:
                        remove_targets.append(target)

                # disconnect remove targets
                for target in remove_targets:
                    target.as_leaf_class().disconnect_content(obj)

class PublisherInlineModelAdmin(InlineModelAdmin):
    form = PublisherAdminForm

class PublisherStackedInline(PublisherInlineModelAdmin, admin.StackedInline):
    pass

class PublisherTabularInline(PublisherInlineModelAdmin, admin.TabularInline):
    pass

class ViewAdminForm(forms.ModelForm):
    page = forms.ChoiceField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(ViewAdminForm, self).__init__(*args, **kwargs)
        self.fields['page'].choices = self.get_page_choices()

    def get_page_choices(self):
        """
        generate page choices from url patterns
        """
        root_urlconf = __import__(settings.ROOT_URLCONF, globals(), locals(), ['urlpatterns',])
        page_choices = [('', '---------'),]
        for pattern in root_urlconf.urlpatterns:
            try:
                page_choices.append((pattern.name, pattern.name.title().replace('_', ' ')))
            except AttributeError:
                pass
        return page_choices
    
class ViewAdmin(admin.ModelAdmin):
    form = ViewAdminForm
