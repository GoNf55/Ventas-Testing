from django.db import models

from clientes.models import Cliente
from stock.models import Producto



class DetalleVenta(models.Model):
    id_detalle_venta = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    # subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.
    
class Venta (models.Model):
    id_venta = models.AutoField(primary_key=True)
    detalleVenta = models.ManyToManyField( DetalleVenta, related_name='Detalles')
    fecha_venta = models.DateField()
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    