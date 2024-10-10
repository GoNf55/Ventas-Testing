# tests.py
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from .models import Producto, Categoria

class ProductoIntegrationTest(TestCase):

    def setUp(self):
        # Crear una categoría para los productos
        self.categoria = Categoria.objects.create(nombre="Categoria 1", descripcion="Descripción de categoría")

        # Crear productos iniciales
        self.producto_1 = Producto.objects.create(
            nombre="Producto 1",
            descripcion="Descripción producto 1",
            categoria=self.categoria,
            precio=100.00,
            cantidad=10
        )
        self.producto_2 = Producto.objects.create(
            nombre="Producto 2",
            descripcion="Descripción producto 2",
            categoria=self.categoria,
            precio=150.00,
            cantidad=20
        )

    def test_producto_list_view(self):
        response = self.client.get(reverse('productos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Producto 1")
        self.assertContains(response, "Producto 2")

    def test_producto_creation_view(self):
        data = {
            'nombre': 'Producto Nuevo',
            'descripcion': 'Descripción producto nuevo',
            'categoria': self.categoria.id_categoria,
            'precio': 200.00,
            'cantidad': 5
        }
        response = self.client.post(reverse('addproducto'), data)
        self.assertEqual(response.status_code, 302)  # Redirige a la lista de productos
        self.assertTrue(Producto.objects.filter(nombre='Producto Nuevo').exists())

    def test_producto_modification_view(self):
        data = {
            'nombre': 'Producto Modificado',
            'descripcion': 'Descripción modificada',
            'categoria': self.categoria.id_categoria,
            'precio': 300.00,
            'cantidad': 15
        }
        response = self.client.post(reverse('modproducto', args=[self.producto_1.id_producto]), data)
        self.producto_1.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Redirige a la lista de productos
        self.assertEqual(self.producto_1.nombre, 'Producto Modificado')
        self.assertEqual(self.producto_1.precio, 300.00)

    def test_producto_deletion_view(self):
        response = self.client.get(reverse('delproducto', args=[self.producto_1.id_producto]))
        self.assertEqual(response.status_code, 302)  # Redirige a la lista de productos
        self.assertFalse(Producto.objects.filter(id_producto=self.producto_1.id_producto).exists())

