from django.shortcuts import render, get_object_or_404, redirect
from .models import Venta, DetalleVenta, Producto, Cliente
from .forms import DetalleVentaForm, VentaForm
from django.db.models import Count, Sum

# Create your views here.

def ventas(request):
    lista_ventas= Venta.objects.filter(eliminado=False).order_by('id_venta')
    return render(request, 'ventas/ventas.html', {'ventas_list':lista_ventas})

def add_venta(request):
     productos = Producto.objects.all()
     if request.method == "POST":
          venta_form = VentaForm(request.POST)
          if venta_form.is_valid():
             venta = venta_form.save(commit=False)
             venta.total_venta = 0  # Se calculará después
             venta.save()

             # Obtener los detalles de venta del frontend
             detalles = request.POST.getlist('detalles')
             total_venta = 0

             for detalle in detalles:
               producto_id, cantidad = detalle.split(',')
               producto = Producto.objects.get(id_producto=producto_id)
               cantidad = int(cantidad)
               subtotal = producto.precio * cantidad

               # Crear el DetalleVenta
               DetalleVenta.objects.create(
                   venta=venta,
                   producto=producto,
                   cantidad=cantidad,
                   subtotal=subtotal
               )
                
               # Actualizar stock
               producto.cantidad -= cantidad
               producto.save()
                
               # Calcular total de la venta
               total_venta += subtotal

          venta.total_venta = total_venta
          venta.save()

          return redirect('ventas')  # Redirige a la página de ventas

     else:
          venta_form = VentaForm()

     return render(request, 'ventas/addventa.html', {'venta_form': venta_form, 'productos':productos})

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


def estadisticas_venta(request):
    # Obtener clientes con más ventas, ordenados de mayor a menor
    clientes_con_ventas = Cliente.objects.annotate(
        total_ventas=Count('venta')
    ).order_by('-total_ventas')

    # Identificar el cliente con más ventas
    cliente_con_mas_ventas = clientes_con_ventas.first()

    # Obtener productos más vendidos en términos de cantidad
    productos_mas_vendidos = Producto.objects.annotate(
          total_vendido=Sum('detalleventa__cantidad')
     ).filter(total_vendido__isnull=False).order_by('-total_vendido')

    # Identificar el producto más vendido
    producto_mas_vendido = productos_mas_vendidos.first()


    context = {
        'clientes_con_ventas': clientes_con_ventas,
        'cliente_con_mas_ventas': cliente_con_mas_ventas,
        'productos_mas_vendidos': productos_mas_vendidos,
        'producto_mas_vendido': producto_mas_vendido,
     }
    return render (request, 'ventas/statsventas.html', context)