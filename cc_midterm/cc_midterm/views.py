from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect

from .forms import UserForm

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

def pie_chart(request):
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

    labels = [x['name'] for x in test_data]
    data = [x['population'] for x in test_data]

    return render(request, 'pie_chart.html', {
        'title': 'Population (test)',
        'labels': labels,
        'data': data,
    })
