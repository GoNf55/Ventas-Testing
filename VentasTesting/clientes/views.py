from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClienteForm
from .models import Cliente
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def clientes(request):
    lista_clientes=Cliente.objects.all().order_by('apellido')
    return render(request, "clientes/clientes.html", {'clientes_list': lista_clientes})

@login_required
def add_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/addcliente.html', {'form': form})

@login_required
def mod_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id_cliente=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/modcliente.html', {'form': form, 'cliente': cliente})

@login_required
def del_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id_cliente=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('clientes')
    return render(request, 'clientes/del_cliente.html', {'cliente': cliente})