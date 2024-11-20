from django.test import TestCase
from stock.models import Categoria, Producto
from django.urls import reverse
from time import time
from django.contrib.auth.models import User

class PerformanceTests(TestCase):
    '''
    Clase para pruebas de rendimiento en la aplicación. Estas pruebas están diseñadas
    para verificar que las operaciones principales sean lo suficientemente rápidas 
    para cumplir con los requisitos de rendimiento.

    En Django, el decorador @classmethod se usa en métodos que pertenecen a la 
    clase en lugar de una instancia de la clase. Esto es especialmente útil en el 
    contexto de pruebas automatizadas, donde ciertas configuraciones iniciales se
    deben realizar una vez por clase y estar disponibles para todas las pruebas 
    que forman parte de esa clase.
    '''

    @classmethod
    def setUpTestData(cls):
        # Configuración inicial de datos para todas las pruebas de rendimiento.
        # Esto crea una categoría de prueba y 100 productos asociados.

        cls.categoria = Categoria.objects.create(
            nombre="Categoria Performance",  # Nombre de la categoría
            descripcion="Descripción de rendimiento"  # Descripción de la categoría
        )
        
        # Creación masiva de 100 productos asociados a la categoría creada.
        productos = [
            Producto(
                nombre=f'Producto {i}',  # Nombre único para cada producto
                precio=10.0,  # Precio inicial para todos los productos
                cantidad=50,  # Cantidad en inventario
                categoria=cls.categoria  # Asociación con la categoría creada
            )
            for i in range(100)
        ]
        Producto.objects.bulk_create(productos)  # Inserción masiva en la base de datos
        # Crear y autenticar un usuario para las pruebas
        cls.user = User.objects.create_user(username='testuser', password='password')

    def setUp(self):
        # Iniciar sesión con el usuario creado
        self.client.login(username='testuser', password='password')    


    def test_page_load_time(self):
        """
        Verificar que la página de listado de productos se cargue en un tiempo aceptable.
        """

        # Registrar el tiempo inicial antes de realizar la solicitud
        start_time = time()
        
        # Realizar una solicitud GET a la URL de listado de productos
        response = self.client.get(reverse('productos'))  # Asegúrate de que esta URL esté configurada
        
        # Registrar el tiempo final después de que se completa la solicitud
        end_time = time()
        
        # Asegurar que la respuesta tenga un estado HTTP 200 (éxito)
        self.assertEqual(response.status_code, 200)
        
        # Comprobar que el tiempo de carga de la página sea menor a 1 segundo
        self.assertLess(
            end_time - start_time, 1, 
            "La carga de la página de productos es demasiado lenta."
        )

    def test_bulk_update_products(self):
        """
        Verificar que se pueda realizar una actualización masiva de productos rápidamente.
        """

        # Obtener todos los productos de la base de datos
        productos = Producto.objects.all()
        
        # Incrementar el precio de cada producto en 5 unidades
        for producto in productos:
            producto.precio += 5
        
        # Registrar el tiempo inicial antes de realizar la actualización masiva
        start_time = time()
        
        # Realizar la actualización masiva en la base de datos para el campo 'precio'
        Producto.objects.bulk_update(productos, ['precio'])
        
        # Registrar el tiempo final después de que se completa la actualización
        end_time = time()
        
        # Comprobar que la actualización masiva se complete en menos de 2 segundos
        self.assertLess(
            end_time - start_time, 2, 
            "La actualización masiva de productos es demasiado lenta."
        )
