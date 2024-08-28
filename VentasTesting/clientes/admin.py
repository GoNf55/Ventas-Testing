from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import Cliente

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id_cliente','apellido','nombre', 'email', 'telefono', )  # Campos que se mostrarán en la lista de clientes
    search_fields = ('nombre', 'apellido',)  # Campos por los que se puede buscar
    list_filter = ('email',)  # Filtros laterales

admin.site.register(Cliente, ClienteAdmin)
