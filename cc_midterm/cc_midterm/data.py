# File for containing any additional data processing for graphs/charts
# Each should return a dict containing 'data' and 'label' fields
# All remaining configuration should be handled within views

import calendar

def get_monthly_transaction_amt(transactions):
    # Accumulate monthly data
    month_dict = {}
    for transaction in transactions:
        month = transaction.purchase.month
        month_name = calendar.month_name[month]
        year = transaction.purchase.year

        if year not in month_dict: month_dict[year] = {}
        if month not in month_dict[year]: month_dict[year][month] = 0
        month_dict[year][month] += transaction.spend

    # Parse monthly data into array of data points and their labels
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
