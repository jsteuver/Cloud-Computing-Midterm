from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django_tables2 import RequestConfig

from .models import Households, Products, Transactions
from .forms import *
from .data import *
from .models import *
from .tables import *
from .uploads import *

# Central UI colors
# Obtained from pastel colors (top row) of:
# https://flatuicolors.com/palette/ru
FLAT_UI_COLORS = [
    '#f3a683', '#f7d794', '#778beb', '#e77f67', '#cf6a87',
    '#786fa6', '#f8a5c2', '#63cdda', '#ea8685', '#596275'
]

# HSHD values to use for analysis
HSHD_VALS = [10, 99, 117, 136, 308]

# Get any data right at the start
# Makes server start a slower, but user can view pages much more quickly
print('Retrieving transaction data (this may take a while)...')
MONTHLY_TRANSACTION_AMT = get_monthly_transaction_amt()
MONTHLY_TRANSACTION_BY_HSHD = get_monthly_transaction_amt_by_hshd(HSHD_VALS)

COMM_TRANSACTION_AMT = get_comm_transaction_amt()
COMM_TRANSACTION_AMT_BY_INCOME = get_comm_transaction_amt_by_income()

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

def engagement_over_time(request):
    # Process total data
    labels = MONTHLY_TRANSACTION_AMT['labels']
    all_data = MONTHLY_TRANSACTION_AMT['data']

    all_data_props = {
        'id': 'all-data',
        'title': 'Cumulative Purchases',
        'xLabel': 'Date',
        'yLabel': 'Purchase Total ($)',
        'labels': labels,
        'datasets': [{'label': 'All Data', 'data': all_data, 'borderColor': FLAT_UI_COLORS[0]}],
    }

    # Process per-household data
    hshd_vals = list(MONTHLY_TRANSACTION_BY_HSHD.keys())
    per_house_dicts = MONTHLY_TRANSACTION_BY_HSHD.values()

    per_house_data_lists = [o['data'] for o in per_house_dicts]

    per_house_datasets = [
        {'label': 'HSHD %d' % h, 'data': l, 'borderColor': FLAT_UI_COLORS[i]} \
        for i, (h, l) in enumerate(zip(hshd_vals, per_house_data_lists))
    ]

    per_house_props = {
        'id': 'per-house',
        'title': 'Per-House Purchases',
        'xLabel': 'Date',
        'yLabel': 'Purchase Total ($)',
        'labels': labels,
        'datasets': per_house_datasets,
    }

    # Render resulting view
    return render(request, 'engagement_over_time.html', {
        'hshd_vals': hshd_vals,
        'all_data_props': all_data_props,
        'per_house_props': per_house_props,
    })
    
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        
        # Before processing, make sure the file exists and is a .csv file

        if 'households' in request.FILES.keys() and request.FILES['households'].name.endswith('.csv'):
            households_file = request.FILES['households'].open('r').read().decode('utf-8')
            upload_households(households_file)
        
        if 'products' in request.FILES.keys() and request.FILES['products'].name.endswith('.csv'):
            products_file = request.FILES['products'].open('r').read().decode('utf-8')
            upload_products(products_file)

        if 'transactions' in request.FILES.keys() and request.FILES['transactions'].name.endswith('.csv'):
            transactions_file = request.FILES['transactions'].open('r').read().decode('utf-8')
            upload_transactions(transactions_file)

        return redirect('data-table')

    else:
        form = UploadForm()
    
    return render(request, 'upload.html', { 'form': form })

def engagement_per_factor(request):
    # Get general data
    commodities = COMM_TRANSACTION_AMT['labels']
    amts_per_household = COMM_TRANSACTION_AMT['data']

    commodity_props = {
        'id': 'commodity',
        'title': 'Commodity Purchases Per Household',
        'xLabel': 'Category',
        'yLabel': 'Purchase Amount Per Household ($)',
        'labels': commodities,
        'datasets': [
            {
                'label': 'All Households',
                'data': amts_per_household,
                'backgroundColor': FLAT_UI_COLORS[0]
            },
        ],
    }

    # Get data split further based on income
    income_ranges = list(COMM_TRANSACTION_AMT_BY_INCOME.keys())
    income_dicts = COMM_TRANSACTION_AMT_BY_INCOME.values()

    income_data_lists = [o['data'] for o in income_dicts]
    color_len = len(FLAT_UI_COLORS)

    per_house_datasets = [
        {'label': ir.strip(), 'data': l, 'backgroundColor': FLAT_UI_COLORS[i % color_len]} \
        for i, (ir, l) in enumerate(zip(income_ranges, income_data_lists))
    ]

    income_props = {
        'id': 'income',
        'title': 'Commodity Purchases Per Household By Income Range',
        'xLabel': 'Category',
        'yLabel': 'Purchase Amount Per Household ($)',
        'labels': commodities,
        'datasets': per_house_datasets,
    }

    # Render resulting view
    return render(request, 'engagement_per_factor.html', {
        'commodity_props': commodity_props,
        'income_props': income_props,
    })

def data_table(request):
    selection = int(request.GET.get('hshd') or 10)
    
    table = DataTable(Transactions.objects.filter(hshd_num=selection))
    hshd_vals = Households.objects.all().order_by('pk')
    RequestConfig(request).configure(table)

    return render(request, 'data_table.html', { 
        'selection': selection,
        'hshd_vals': hshd_vals,
        'table': table 
    })