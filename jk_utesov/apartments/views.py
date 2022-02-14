from django.shortcuts import render
from django.http import HttpResponse
from .models import *


def index(request):
    apartments = Apartment.objects.all()
    return render(request, 'apartments/index.html',
                  {'apartments': apartments, 'title': 'Стартовая страница системы пропусков ЖК "Утёсов"'})


def list_residents(request):
    residents = Resident.objects.all()
    return render(request, 'apartments/list_resident.html',
                  {'residents': residents, 'title': 'Список жителей ЖК "Утёсов"'})
