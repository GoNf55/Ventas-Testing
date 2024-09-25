from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductoForm, CategoriaForm
from .models import Producto, Categoria

# Create your views here.


# ABM productos
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
        form = ProductoForm(request.POST, instance=producto)
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

#ABM Categorias
def categorias(request):
    lista_categorias=Categoria.objects.all().order_by('nombre')
    return render(request,'stock/categorias.html', {'listado_categorias':lista_categorias})

def addcategorias(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorias')
    else:
        form = CategoriaForm()
    return render(request, 'stock/addcategorias.html', {'form':form}  )

def modcategorias(request, categoria_id):
    categoria = get_object_or_404(Categoria, id_categoria=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'stock/modcategorias.html', {'form': form, 'categoria': categoria})

def delcategorias(request, categoria_id):
    categoria = get_object_or_404(Categoria, id_categoria=categoria_id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categorias')
    return render(request, 'stock/categorias.html', {'categoria': categoria})