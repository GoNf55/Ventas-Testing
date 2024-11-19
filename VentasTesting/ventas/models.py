from django.db import models

from clientes.models import Cliente
from stock.models import Producto

    
class Venta (models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha_venta = models.DateField()
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    eliminado = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.id_venta} - {self.cliente.nombre} - {self.fecha_venta}"
class DetalleVenta(models.Model):
    id_detalle_venta = models.AutoField(primary_key=True)
    venta = models.ForeignKey(Venta, related_name='detalleVenta', on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.id_detalle_venta} - {self.producto.nombre} x {self.cantidad}"