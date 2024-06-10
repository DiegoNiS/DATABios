# Proyecto/views.py
# Para pruebas con los templates, pse puede eliminar
from django.shortcuts import render

def home(request):
    return render(request, 'base.html')
