# File for containing any additional data processing for graphs/charts
# Each should return a dict containing 'data' and 'label' fields
# All remaining configuration should be handled within views

import calendar
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from .models import Households, Products, Transactions

def get_monthly_transaction_amt(transactions=None):
    if transactions is None: transactions = Transactions.objects.all()

    grouped = Transactions.objects \
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
