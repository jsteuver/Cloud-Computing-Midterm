# File for containing any additional data processing for graphs/charts
# Each should return a dict containing 'data' and 'label' fields
# All remaining configuration should be handled within views

import calendar

from .models import Households, Products, Transactions

def get_monthly_transaction_amt():
    print('Getting monthly transaction amounts (this may take awhile)...')
    all_transactions = Transactions.objects.all()

    month_dict = {}
    for transaction in all_transactions:
        month = transaction.purchase.month
        month_name = calendar.month_name[month]
        year = transaction.purchase.year

        if year in month_dict:
            if month in month_dict[year]:
                month_dict[year][month] += transaction.spend
            else:
                month_dict[year][month] = transaction.spend
        else:
            month_dict[year] = {}
            month_dict[year][month] = transaction.spend

    data = []
    labels = []

    for year in sorted(month_dict.keys()):
        year_data = month_dict[year]
        for month in sorted(year_data.keys()):
            label_string = calendar.month_name[month] + ' ' + str(year)
            purchase_amt = int(year_data[month])

            labels.append(label_string)
            data.append(purchase_amt)

    return {
        'data': data,
        'labels': labels,
    }
