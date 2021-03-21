from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django_tables2 import RequestConfig

from .models import Households, Products, Transactions
from .forms import UserForm
from .data import get_monthly_transaction_amt
from .models import *
from .tables import *

# Central UI colors
# Obtained from pastel colors (top row) of:
# https://flatuicolors.com/palette/ru
FLAT_UI_COLORS = [
    '#f3a683', '#f7d794', '#778beb', '#e77f67', '#cf6a87',
    '#786fa6', '#f8a5c2', '#63cdda', '#ea8685', '#596275'
]

# Get any data right at the start
# Makes server start a slower, but user can view pages much more quickly
ALL_TRANSACTIONS = Transactions.objects.all()

print('Retrieving transaction data (this may take a while)...')
MONTHLY_TRANSACTION_AMT = get_monthly_transaction_amt(ALL_TRANSACTIONS)

def home(request):
    text = "Welcome! Please log in to continue."
    if request.user.pk:
        text = "Welcome, " + request.user.username + "."

    return render(request, 'index.html', { 'text': text })

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserForm()

    return render(request, 'signup.html', { 'form': form })

def engagement(request):
    data = MONTHLY_TRANSACTION_AMT['data']
    labels = MONTHLY_TRANSACTION_AMT['labels']

    return render(request, 'engagement.html', {
        'title': 'Purchases',
        'labels': labels,
        'data': data,
        'backgroundColor': FLAT_UI_COLORS[8],
        'borderColor': FLAT_UI_COLORS[9],
        'xLabel': 'Date',
        'yLabel': 'Purchase Total ($)',
    })


# === TEMP ===

# Temporary test data
test_data = [
    {
        'id': 1,
        'name': 'Tokyo',
        'country_id': 28,
        'population': 36923000,
    }, {
        'id': 2,
        'name': 'Shanghai',
        'country_id': 13,
        'population': 34000000,
    }, {
        'id': 3,
        'name': 'Jakarta',
        'country_id': 19,
        'population': 30000000,
    }, {
        'id': 4,
        'name': 'Seoul',
        'country_id': 21,
        'population': 25514000,
    }, {
        'id': 4,
        'name': 'Seoul',
        'country_id': 21,
        'population': 25514000,
    }, {
        'id': 4,
        'name': 'Seoul',
        'country_id': 21,
        'population': 25514000,
    }, {
        'id': 4,
        'name': 'Seoul',
        'country_id': 21,
        'population': 25514000,
    }, {
        'id': 4,
        'name': 'Seoul',
        'country_id': 21,
        'population': 25514000,
    }, {
        'id': 4,
        'name': 'Seoul',
        'country_id': 21,
        'population': 25514000,
    }, {
        'id': 4,
        'name': 'Seoul',
        'country_id': 21,
        'population': 25514000,
    }, {
        'id': 5,
        'name': 'Guangzhou',
        'country_id': 13,
        'population': 25000000,
    }]

def home(request):
    text = "Welcome! Please log in to continue."
    if request.user.pk:
        text = "Welcome, " + request.user.username + "."

    return render(request, 'index.html', { 'text': text })

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserForm()

    return render(request, 'signup.html', { 'form': form })

def data_table(request):
    selection = int(request.GET.get('hshd') or 10)
    
    table = DataTable(Transactions.objects.filter(hshd_num=selection))
    hshds = Households.objects.all().order_by('pk')
    RequestConfig(request).configure(table)

    return render(request, 'data_table.html', { 
        'selection': selection,
        'hshds': hshds,
        'table': table 
    })

def pie_chart(request):
    global test_data
    labels = [x['name'] for x in test_data]
    data = [x['population'] for x in test_data]

    return render(request, 'pie_chart.html', {
        'title': 'Population (test)',
        'labels': labels,
        'data': data,
        'backgroundColors': FLAT_UI_COLORS,
    })

def line_chart_labeled(request):
    global test_data
    labels = [x['name'] for x in test_data]
    data = [x['population'] for x in test_data]

    return render(request, 'line_chart_labeled.html', {
        'title': 'Population (test)',
        'labels': labels,
        'data': data,
        'backgroundColor': FLAT_UI_COLORS[8],
        'borderColor': FLAT_UI_COLORS[9],
        'xLabel': 'City',
        'yLabel': 'Population',
    })
