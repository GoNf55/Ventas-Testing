from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductoForm
from .models import Producto

# Create your views here.

def productos(request):
    lista_productos=Producto.objects.all().order_by('nombre')
    return render(request,'stock/productos.html', {'productos_list': lista_productos})

def addproductos(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = ProductoForm()
    return render(request, 'stock/addproductos.html', {'form': form})

def modproductos(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto_id)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'stock/modproductos.html', {'form': form, 'producto': producto})

def delproductos(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos')
    return render(request, 'stock/delproducto.html', {'producto': producto})