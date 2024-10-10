from django.shortcuts import render, get_object_or_404, redirect
from .models import Venta

# Create your views here.

def ventas(request):
    lista_ventas= Venta.objects.filter(eliminado=False).order_by('id_venta')
    return render(request, 'ventas/ventas.html', {'ventas_list':lista_ventas})

def add_venta(request):
     return render(request, 'ventas/addventa.html')

def cons_venta(request ,venta_id):
     venta = get_object_or_404(Venta, id_venta=venta_id)
     detalles = venta.detalleVenta.all()  # Obtener todos los DetalleVenta asociados
     return render(request, 'ventas/consventa.html', {'venta': venta, 'lista_detalles' : detalles})

def del_venta(request, venta_id):
     venta=get_object_or_404(Venta, id_venta=venta_id)
     if request.method == 'POST':
        venta.eliminado=True
        venta.save()
        return redirect('ventas')
     return render(request, 'ventas/venta.html', {'venta': venta})