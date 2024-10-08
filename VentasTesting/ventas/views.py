from django.shortcuts import render
from .models import Venta

# Create your views here.

def ventas(request):
    lista_ventas= Venta.objects.all().order_by('id_venta')
    return render(request, 'ventas/ventas.html', {'ventas_list':lista_ventas})

def add_venta(request):
     return render(request, 'ventas/addventa.html')

def cons_venta(request):
     return render(request, 'ventas/consventa.html')