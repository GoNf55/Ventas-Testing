from django.shortcuts import render
from .models import Venta

# Create your views here.

def ventas(request):
    lista_ventas= Venta.objects.all().order_by('id_venta')
    return render(request, 'ventas/ventas.html', {'ventas_list':lista_ventas})
