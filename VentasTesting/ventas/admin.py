from django.contrib import admin

from .models import DetalleVenta, Venta


# Register your models here.
admin.site.register(Venta)
admin.site.register(DetalleVenta)