from django.contrib import admin

from .models import DetalleVenta, Venta


class VentaAdmin(admin.ModelAdmin):
    list_display = ('id_venta','cliente','fecha_venta', 'total_venta', )  # Campos que se mostrarán en la lista de clientes
    search_fields = ('id_venta',)  # Campos por los que se puede buscar
    list_filter = ('eliminado',)  # Filtros laterales
# Register your models here.
admin.site.register(Venta, VentaAdmin)
admin.site.register(DetalleVenta)