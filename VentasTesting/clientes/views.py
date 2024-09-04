from django.shortcuts import render
from .models import Cliente

# Create your views here.

def clientes(request):
    lista_clientes=Cliente.objects.all()
    return render(request, "clientes/clientes.html", {'clientes_list': lista_clientes})