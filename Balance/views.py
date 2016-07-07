from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from .forms import *
import ipdb
import pandas as pd


# Create your views here.
def index(request):
    return render(request, 'home.html')


class StoreList(ListView):
    model = Store
    template_name = "store.html"


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

    return render(request, 'store.html',
                  {'create_form': create_form, 'delete_form': delete_form, 'store_list': model_objects})


def upload_ing(request):
    form = UploadIngForm(request.GET or None)
    if request.method == 'POST':
        form = UploadIngForm(request.POST, request.FILES)
        if form.is_valid():
            df = uploaded_file_to_dataframe(form.cleaned_data.get('file'))
            df = pre_process_ing_data(df)
            save_transactions(df)
            return HttpResponseRedirect('/prending_transactions')

    return render(request, 'upload.html', {'UploadINGForm': form})


def pre_process_ing_data(df):
    ipdb.set_trace()
    df.rename(columns={'Naam / Omschrijving': 'Description',
                       'Tegenrekening': 'Destination',
                       'Af Bij': 'Sign',
                       'Bedrag (EUR)': 'Amount',
                       'Mededelingen': 'Extra',
                       'Datum': 'Date'
                       }, inplace=True)
    df.Date = pd.to_datetime(df.Date, format="%Y%m%d")
    df['Description'] = df['Description'] + ", " + df['Extra']
    df['Amount'] = df['Amount'].str.replace(',', '.').astype(float)  # convert decimal separator, cast to float
    df.loc[df['Sign'] == 'Af', 'Amount'] *= -1
    # df = df.drop([''])
    del df['Extra']
    del df['Sign']
    del df['Rekening']
    del df['Code']
    del df['MutatieSoort']
    df['Category'] = None
    df['Store'] = None
    df['Processed'] = False
    return df


def save_transactions(df):
    bulk = []
    ipdb.set_trace()
    for row in df.iterrows():
        bulk.append(Transaction(Amount=row[1]['Amount'],
                                Description=row[1]['Description'],
                                Destination=row[1]['Destination'],
                                Category=row[1]['Category'],
                                Store=row[1]['Store'],
                                Processed=row[1]['Processed'],
                                Date=row[1]['Date']))
    Transaction.objects.bulk_create(bulk)
    # 'Datum', 'Description', 'Destination', 'Amount', 'Category', 'Store', 'Processed'
    # Datum = models.DateField()
    # Amount = models.FloatField()
    # Destination = models.CharField(max_length=255)
    # Description = models.CharField(max_length=255)
    # Category = models.ForeignKey(Category)
    # Store = models.ForeignKey(Store)
    # Processed = models.BooleanField()


def upload_ov(request):
    form = UploadOvForm(request.GET or None)
    if request.method == 'POST':
        form = UploadOvForm(request.POST, request.FILES)
        if form.is_valid():
            df = uploaded_file_to_dataframe(form.cleaned_data.get('file'))
    return render(request, 'upload.html', {'UploadOVForm': form})


def pending_transactions(request):
    p_t = None

    # processing by filtering with rules
    # df = pd.DataFrame()
    # rules = [{'Field': 'Description', 'Search': 'albert heijn', 'Category': 'Food', 'Store': 'AH'}]
    # for rule in rules:
    #     mask = df[rule['Field']].str.contains(rule['Search'], case=False)
    #     df.loc[mask, Category] = rule['Category']
    #     df.loc[mask, Store] = rule['Store']
    # pending_form = PendingTransactions()
    from django.forms import modelformset_factory
    ipdb.set_trace()
    # rules_form = modelformset_factory(Rule, )
    pending_form = modelformset_factory(Transaction, exclude=('Processed',), formset=PendingFormSet, extra=0)
    return render(request, 'pending.html', {'pending_transactions': p_t, 'pending_form': pending_form})
    # Add column selector, add regex,


def uploaded_file_to_dataframe(file):
    with open('temp.csv', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
        return pd.read_csv(destination.name)
