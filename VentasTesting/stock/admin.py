from django.contrib import admin
from .models import Producto, Categoria

# Register your models here.
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id_categoria','nombre', 'descripcion')  # Campos que se mostrarán en la lista de clientes
    search_fields = ('nombre',)  # Campos por los que se puede buscar

class ProductoAdmin(admin.ModelAdmin):
    list_display= ('id_producto','nombre','precio','cantidad','descripcion')
    search_fields=('nombre',)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
