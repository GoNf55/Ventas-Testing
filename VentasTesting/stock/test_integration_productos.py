from django.test import TestCase
from django.urls import reverse
from .models import Producto, Categoria

class ProductoIntegrationTests(TestCase):
    def setUp(self):
        # Crear una categoría para usar en los productos
        self.categoria = Categoria.objects.create(nombre="electronica", descripcion="dispositivos electronicos")
        
        # Crear productos para las pruebas
        self.producto1 = Producto.objects.create(
            nombre="notebook",
            descripcion="notebook de alta gama",
            categoria=self.categoria,
            precio=1500.00,
            cantidad=10
        )
        
        self.producto2 = Producto.objects.create(
            nombre="celular",
            descripcion="celular con pantalla HD",
            categoria=self.categoria,
            precio=800.00,
            cantidad=5
        )

    def test_listar_productos(self):
        # Acceder a la vista de listar productos
        response = self.client.get(reverse('productos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stock/productos.html')
        self.assertContains(response, self.producto1.nombre)
        self.assertContains(response, self.producto2.nombre)

    def test_agregar_producto(self):
        # Datos del nuevo producto
        data = {
            'nombre': 'tablet',
            'descripcion': 'tablet de 10 pulgadas',
            'categoria': self.categoria.id_categoria,
            'precio': 300.00,
            'cantidad': 20
        }
        
        # Enviar datos a la vista de agregar producto
        response = self.client.post(reverse('addproducto'), data)
        self.assertEqual(response.status_code, 302)  # Redirección a la lista de productos
        
        # Verificar que el producto fue agregado correctamente
        self.assertTrue(Producto.objects.filter(nombre='tablet').exists())

    def test_modificar_producto(self):
        # Datos modificados para producto1
        data = {
            'nombre': 'notebook actualizada',
            'descripcion': 'notebook de alta gama actualizada',
            'categoria': self.categoria.id_categoria,
            'precio': 1600.00,
            'cantidad': 8
        }
        
        # Enviar datos de modificación
        response = self.client.post(reverse('modproducto', args=[self.producto1.id_producto]), data)
        self.assertEqual(response.status_code, 302)  # Redirección a la lista de productos
        
        # Verificar que los cambios se guardaron
        self.producto1.refresh_from_db()
        self.assertEqual(self.producto1.nombre, 'notebook actualizada')
        self.assertEqual(self.producto1.precio, 1600.00)

    def test_eliminar_producto(self):
        # Enviar solicitud para eliminar producto1
        response = self.client.post(reverse('delproducto', args=[self.producto1.id_producto]))
        self.assertEqual(response.status_code, 302)  # Redirección a la lista de productos
        
        # Verificar que el producto fue eliminado
        self.assertFalse(Producto.objects.filter(id_producto=self.producto1.id_producto).exists())
