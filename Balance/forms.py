from django import forms
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
    Store = forms.ModelChoiceField(queryset=Store.objects.all().values('Store').values_list('Store',flat=True))


class AddCategory(forms.Form):
    Category = forms.CharField(max_length=255)
