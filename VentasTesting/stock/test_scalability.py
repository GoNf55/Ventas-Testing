from django.test import TestCase
from stock.models import Categoria, Producto
from django.urls import reverse
from django.contrib.auth.models import User

class ScalabilityTests(TestCase):
    """
    Clase para pruebas de escalabilidad en la aplicación. Estas pruebas verifican si
    el sistema puede manejar grandes volúmenes de datos y operaciones de manera eficiente.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Configuración inicial de datos para todas las pruebas de escalabilidad. 
        Crea una categoría y un conjunto de 1000 productos para probar el rendimiento del sistema.
        """
        # Crear una categoría para asociarla a los productos de prueba
        cls.categoria = Categoria.objects.create(
            nombre="Categoria Escalabilidad",  # Nombre de la categoría
            descripcion="Descripción de escalabilidad"  # Descripción de la categoría
        )
        
        # Crear 1000 productos asociados a la categoría creada
        productos = [
            Producto(
                nombre=f'Producto Escalable {i}',  # Nombre único para cada producto
                precio=10.0,  # Precio inicial para todos los productos
                cantidad=50,  # Cantidad en inventario
                categoria=cls.categoria  # Asociación con la categoría creada
            )
            for i in range(1000)
        ]
        Producto.objects.bulk_create(productos)  # Inserción masiva en la base de datos
        # Crear y autenticar un usuario para las pruebas
        cls.user = User.objects.create_user(username='testuser', password='password')

    def setUp(self):
        # Iniciar sesión con el usuario creado
        self.client.login(username='testuser', password='password')    


    def test_large_number_of_products_handling(self):
        """
        Verificar que la aplicación maneje una gran cantidad de productos sin errores.
        """
        # Realizar una solicitud GET a la URL de listado de productos
        response = self.client.get(reverse('productos'))
        
        # Asegurar que la respuesta tenga un estado HTTP 200 (éxito)
        self.assertEqual(response.status_code, 200)
        
        # Verificar que el último producto sea accesible en la página
        self.assertContains(response, 'Producto Escalable 999')
        
        # Verificar que el primer producto también sea accesible en la página
        self.assertContains(response, 'Producto Escalable 0')

    def test_create_large_number_of_products(self):
        """
        Verificar que la base de datos pueda manejar la creación masiva de productos.
        """
        # Crear 500 nuevos productos asociados a la categoría
        productos = [
            Producto(
                nombre=f'Nuevo Producto Escalable {i}',  # Nombre único para cada nuevo producto
                precio=15.0,  # Precio inicial para los nuevos productos
                cantidad=30,  # Cantidad en inventario
                categoria=self.categoria  # Asociación con la categoría creada
            )
            for i in range(500)
        ]
        
        # Insertar los nuevos productos en la base de datos
        Producto.objects.bulk_create(productos)
        
        # Verificar que ahora haya un total de 1500 productos en la base de datos
        self.assertEqual(Producto.objects.count(), 1500)

