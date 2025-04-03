# from django.http import HttpResponse
from django.shortcuts import render
from customers.models import Customer
from books.models import Book

def home_view(request):
    qs = Customer.objects.all()
    try:
        obj = Book.objects.get(id=2)
        books = obj.title.get_books()
    except Book.DoesNotExist:
        obj = None
        books = []
    context = {
        'qs': qs,
        'obj': obj,
        'books': books,
    }
    return render(request, 'main.html', context)