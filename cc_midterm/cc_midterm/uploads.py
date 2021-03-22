from .models import *


def upload_households(households_file):
    households_rows = households_file.split('\n')

    households = []
    for i in range(1, len(households_rows)):
        if households_rows[i] == '': # Empty row: just move on to the next one
            continue

        row_values = households_rows[i].split(',')

        h = Households(
                hshd_num=int(row_values[0].strip()),
                l=row_values[1],
                age_range=row_values[2],
                marital=row_values[3],
                income_range=row_values[4],
                homeowner=row_values[5],
                hshd_composition=row_values[6],
                hh_size=row_values[7],
                children=row_values[8]
            )

        households.append(h)
        
        # Households.objects.bulk_update_or_create(households, ['l', 'age_range', 'marital', 'income_range', 'homeowner', 'hshd_composition', 'hh_size', 'children'], match_field='hshd_num')

def upload_products(products_file):
    products_rows = products_file.split('\n')

    products = []
    for i in range(1, len(products_rows)):
        if products_rows[i] == '': # Empty row: just move on to the next one
            continue

        row_values = products_rows[i].split(',')

        p = Products(
                product_num=int(row_values[0].strip()),
                department=row_values[1],
                commodity=row_values[2],
                brand_ty=row_values[3],
                natural_organic_flag=row_values[4]
            )

        products.append(p)

        # Products.objects.bulk_update_or_create(products, ['department', 'commodity', 'brand_ty', 'natural_organic_flag'], match_fields='product_num')

def upload_transactions(transactions_file):
    transactions_rows = transactions_file.split('\n')

    transactions = []
    for i in range(1, len(transactions_rows)):
        if transactions_rows[i] == '': # Empty row: just move on to the next one
            continue

        row_values = transactions_rows[i].split(',')

        p = transactions(
                basket_num=int(row_values[0].strip()),
                hshd_num=row_values[1],
                purchase=row_values[2],
                product_num=row_values[3],
                spend=row_values[4],
                units=row_values[5],
                store_r=row_values[6],
                week_num=row_values[7],
                year=row_values[8]
            )

        transactions.append(p)

        # transactions.objects.bulk_update_or_create(transactions, ['hshd_num', 'purchase', 'product_num', 'spend', 'units', 'store_r', 'week_num', 'year'], match_fields='basket_num')
