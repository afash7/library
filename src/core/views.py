# from django.http import HttpResponse
from django.shortcuts import render


def home_view(request):
    name = 'Afash'
    return render(request, 'main.html', {'show_name': name})