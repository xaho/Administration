from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .forms import *
import ipdb
import pandas as pd
import tempfile


# Create your views here.
def index(request):
    return render(request, 'index.html')


class StoreList(ListView):
    model = Store
    template_name = "index.html"


def stores(request):
    create_form = CreateStore(request.GET or None)
    delete_form = RemoveStore(request.GET or None)
    model_objects = Store.objects.all()
    if request.method == 'POST':
        ipdb.set_trace()
        if 'create' in request.POST:
            create_form = CreateStore(request.POST or None)
            if create_form.is_valid():
                store = Store(Store=create_form.cleaned_data.get('Store'))
                store.save()
        elif 'delete' in request.POST:
            delete_form = RemoveStore(request.POST or None)
            if delete_form.is_valid():
                Store.objects.get(Store=create_form.cleaned_data.get('Store')).delete()

    return render(request, 'index.html',
                  {'create_form': create_form, 'delete_form': delete_form, 'store_list': model_objects})


def upload_ov(request):
    form = UploadOvForm(request.GET or None)
    if request.method == 'POST':
        form = UploadOvForm(request.POST, request.FILES)
        if form.is_valid():
            df = uploaded_file_to_dataframe(form.cleaned_data.get('file'))
    return render(request, 'index.html', {'UploadOVForm': form})


def uploaded_file_to_dataframe(file):
    with open('temp.csv', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
        return pd.read_csv(destination.name)


def pre_process_ing_data(df):
    del df['Code']
    del df['MutatieSoort']
    df.rename(columns={'Af Bij': 'Sign',
                       'Bedrag (EUR)': 'Amount',
                       'Rekening': 'To',
                       'Banknumber': 'From',
                       'Naam / Omschrijving': 'Description',
                       'Mededelingen': 'Extra'
                       }, inplace=True)

    df['Amount'] = df['Amount'].str.replace(',','.').astype(float)  # convert decimal separator, cast to float
    df.loc[df['Sign'] == 'Af', 'Amount'] *= -1
    del df['Sign']
    del df['To']
    df['Category'] = ''
    df['Store'] = ''

    # processing by filtering with rules
    ipdb.set_trace()
    rules = [{'Field':'Description', 'Search': 'albert heijn', 'Category': 'Food', 'Store': 'AH'}]
    for rule in rules:
        mask = df[rule['Field']].str.contains(rule['Search'],case=False)
        df[mask].Category = rule['Category']
        df[mask].Store = rule['Store']


def upload_ing(request):
    form = UploadIngForm(request.GET or None)
    if request.method == 'POST':
        form = UploadIngForm(request.POST, request.FILES)
        if form.is_valid():
            df = uploaded_file_to_dataframe(form.cleaned_data.get('file'))
            pre_process_ing_data(df)
            return

    return render(request, 'index.html', {'UploadINGForm': form})


def process_ing(request):
    return render(request, 'index.html')