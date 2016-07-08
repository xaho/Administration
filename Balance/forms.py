from django import forms
from django.apps import apps
from .models import *


class UploadIngForm(forms.Form):
    file = forms.FileField()


class UploadOvForm(forms.Form):
    file = forms.FileField()


class ApplyRules(forms.Form):
    Field = forms.CharField(max_length=255)
    Search = forms.CharField(max_length=255)
    Category = forms.ModelChoiceField(queryset=Category.objects.all())
    Store = forms.ModelChoiceField(queryset=Store.objects.all())


class CreateStore(forms.Form):
    Store = forms.CharField(max_length=255)

    def clean(self):
        cleaned_data = super(CreateStore, self).clean()
        store = cleaned_data.get('Store')
        if len(Store.objects.filter(Store=store)) > 0:
            raise forms.ValidationError("Store already exists.")


class RemoveStore(forms.Form):
    Store = forms.ModelChoiceField(queryset=Store.objects.all().values_list('Store', flat=True))


class AddCategory(forms.Form):
    Category = forms.CharField(max_length=255)


class FilterForm(forms.Form):
    # choices = [field.name for field in Transaction._meta.get_fields() if field.name in]
    choices = ['Store', 'Category']
    filter_column = forms.ChoiceField(choices=[(choice, choice) for choice in choices])
    filter = forms.CharField()


class AssignForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        fields = [field.name for field in Transaction._meta.get_fields() if type(field) is models.ForeignKey]
        for field in fields:
            self.fields[field] = forms.ModelChoiceField(
                queryset=apps.get_app_config('Balance').get_model(field).objects.all().values_list(field, flat=True),
                to_field_name=field)
