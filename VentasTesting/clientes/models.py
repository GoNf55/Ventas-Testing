from django.db import models

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=20)
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
    
