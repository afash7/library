# from django.http import HttpResponse
from django.shortcuts import render
from customers.models import Customer
from books.models import Book

def home_view(request):
    qs = Customer.objects.all()
    try:
        obj = Book.objects.get(id=2)
    except Book.DoesNotExist:
        obj = None
    context = {
        'qs': qs,
        'obj': obj,
    }
    return render(request, 'main.html', context)