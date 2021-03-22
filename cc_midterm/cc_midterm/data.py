# File for containing any additional data processing for graphs/charts
# Each should return a dict containing 'data' and 'label' fields
# All remaining configuration should be handled within views

import calendar
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from .models import Households, Products, Transactions

def get_monthly_transaction_amt(transactions=None):
    if transactions is None: transactions = Transactions.objects.all()

    grouped = transactions \
                          .annotate(month=TruncMonth('purchase')) \
                          .values('month') \
                          .annotate(total=Sum('spend')) \
                          .order_by('month')

    raw_data = grouped.values_list('total', flat=True)
    raw_dates = grouped.values_list('month', flat=True)

    data = [float(x) for x in raw_data]
    labels = ['%s %d' % (calendar.month_name[d.month], d.year) for d in raw_dates]

    return {
        'data': data,
        'labels': labels,
    }

def get_monthly_transaction_amt_by_hshd(hshd_vals, transactions=None):
    if transactions is None: transactions = Transactions.objects.all()

    ret_dict = {}
    for hshd in hshd_vals:
        print('Retrieving transactions for HSHD:', hshd)
        this_hshd_transactions = transactions.filter(hshd_num=hshd)
        ret_dict[hshd] = get_monthly_transaction_amt(this_hshd_transactions)

    return ret_dict
