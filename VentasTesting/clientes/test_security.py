from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from appCore.forms import CustomUserCreationForm  # Asumí que el formulario de login es CustomUserCreationForm
from clientes.models import Cliente
from ventas.models import Venta, DetalleVenta
from stock.models import Categoria, Producto

class SecurityTests(TestCase):

    def setUp(self):
        # Crear un cliente para las pruebas de venta
        self.cliente = Cliente.objects.create(
            nombre='Juan',
            apellido='Pérez',
            email='juan@example.com',
            telefono='123456789',
            dni='12345678'
        )
        #se crea una categoria para asignarsela a un producto
        self.categoria = Categoria.objects.create(
            nombre="Categoria Test",
            descripcion="Descripción de prueba para la categoría"
        )
        
        # Crear un producto de prueba y asociarlo a la categoría creada
        self.producto = Producto.objects.create(
            nombre='Producto Test',
            precio=100.0,
            cantidad=10,
            categoria=self.categoria
        )
        
        # Crear una venta de prueba y asociarla al cliente creado
        self.venta = Venta.objects.create(
            cliente=self.cliente,
            total_venta=200.0,  
            fecha_venta='2024-11-01'  
        )
        
        # Crear un detalle de venta y añadirlo a la venta creada
        self.detalle_venta = DetalleVenta.objects.create(
            producto=self.producto,
            cantidad=2,
            subtotal=200.0
        )
        self.venta.detalleVenta.add(self.detalle_venta)

        # Crear un usuario de prueba para los tests de autenticación
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='testuser'
        )

        # Guardar las URLs para la prueba de login y la página principal
        self.login_url = reverse('login')  # URL de inicio de sesión
        self.home_url = reverse('home')  # URL de la página de inicio

    def test_login_success(self):
        # Verificar que un usuario con credenciales correctas puede iniciar sesión.
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertRedirects(response, self.home_url)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_failure(self):
        #Verificar que un usuario con credenciales incorrectas recibe un mensaje de error y no puede iniciar sesión. 
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Por favor, introduzca un nombre de usuario y clave correctos. Observe que ambos campos pueden ser sensibles a mayúsculas.")
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_protected_view_without_login(self):
        #Verificar que los usuarios no autenticados no puedan acceder a vistas protegidas.
        response = self.client.get(self.home_url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'{self.login_url}?next={self.home_url}')

    def test_access_protected_view_after_login(self):
        #Verificar que un usuario autenticado pueda acceder a vistas protegidas.
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bienvenido testuser !")

    def test_sql_injection_attempt(self):
        #Verificar que la aplicación es resistente a ataques de inyección SQL. 
        # Intentar hacer un SQL Injection en el login
        response = self.client.post(self.login_url, {
            'username': 'testuser\' OR 1=1 --',  # Intento de inyección SQL en el nombre de usuario
            'password': 'any'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Por favor, introduzca un nombre de usuario y clave correctos.")

    def test_xss_injection_attempt(self):
        # Verificar que la aplicación es resistente a ataques de XSS (Cross-Site Scripting). 
        # Intentar inyectar un script en el nombre del cliente para probar vulnerabilidades de XSS
        response = self.client.post(self.login_url, {
            'username': '<script>alert("XSS")</script>',  # Intento de XSS en el nombre de usuario
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'alert("XSS")')  # Verifica que el script no se ejecute

    def test_venta_integrity(self):
        #Verificar que la venta esté correctamente asociada al cliente y al detalle de venta. 
        # Comprueba que el cliente asociado a la venta es correcto
        self.assertEqual(self.venta.cliente, self.cliente)
        # Verifica el total de la venta
        self.assertEqual(self.venta.total_venta, 200.0)
        # Verifica que la venta tiene el detalle asociado
        self.assertEqual(self.venta.detalleVenta.count(), 1)
        # Confirma que el producto en el detalle de venta es el esperado
        self.assertEqual(self.detalle_venta.producto, self.producto)
