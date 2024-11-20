from django.test import TestCase
from django.urls import reverse
from .models import Cliente
from django.contrib.auth.models import User  # Para crear usuarios

class ClienteViewsTest(TestCase):
    
    def setUp(self):

        # Crear un usuario y autenticarlo
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        
        # Crear un cliente para usar en las pruebas
        self.cliente = Cliente.objects.create(
            nombre="Naruto",
            apellido="Uzumaki",
            email="naru.uzu@example.com",
            telefono="676767676"
        )

    def test_crear_cliente_con_campos_validos(self):
        # Verificar que un usuario puede crear un nuevo cliente con los campos obligatorios llenados correctamente
        response = self.client.post(reverse('addcliente'), {
            'nombre': 'María',
            'apellido': 'López',
            'email': 'maria.lopez@example.com',
            'telefono': '987654321'
        })
        self.assertEqual(response.status_code, 302)  # redirige a la lista de clientes
        self.assertEqual(Cliente.objects.count(), 2)


    def test_crear_cliente_sin_campos_obligatorios(self):
        # Verificar que un usuario recibe un mensaje de error al intentar crear un cliente sin llenar los campos obligatorios
        response = self.client.post(reverse('addcliente'), {
            'nombre': '',
            'apellido': '',
            'email': '',
            'telefono': ''
        })
        self.assertEqual(response.status_code, 200)  # No redirige, sigue en la misma página
        self.assertContains(response, "Este campo es obligatorio.")  # Verifica que se muestra el error
        self.assertEqual(Cliente.objects.count(), 1)  # Solo debe haber un cliente (el creado en setUp)

    def test_ver_detalle_cliente_existente(self):
        # Verificar que un usuario puede ver el detalle de un cliente existente
        response = self.client.get(reverse('modcliente', args=[self.cliente.id_cliente]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.cliente.nombre)
    
    def test_modificar_cliente_existente(self):
        # Verificar que un usuario puede editar un cliente existente y que los cambios se guardan correctamente
        response = self.client.post(reverse('modcliente', args=[self.cliente.id_cliente]), {
            'nombre': 'Carlos',
            'apellido': 'González',
            'email': 'carlos.gonzalez@example.com',
            'telefono': '123123123'
        })
        self.cliente.refresh_from_db()
        self.assertEqual(self.cliente.nombre, 'Carlos')
        self.assertEqual(response.status_code, 302)  # redirige a la lista de clientes

    def test_eliminar_cliente(self):
        # Verificar que un usuario puede eliminar un cliente y que el registro se elimina de la base de datos
        response = self.client.post(reverse('delcliente', args=[self.cliente.id_cliente]))
        self.assertEqual(response.status_code, 302)  # redirige a la lista de clientes
        self.assertEqual(Cliente.objects.count(), 0)  # No debe quedar ningún cliente en la base de datos
        
    def test_crear_cliente_con_error_intencional(self):
        # Este test está diseñado para fallar
        response = self.client.post(reverse('addcliente'), {
            'nombre': 'Carlos',
            'apellido': 'González',
            'email': 'carlos.gonzalez@example.com',
            'telefono': '987654321'
        })
        self.assertEqual(Cliente.objects.count(), 100)  # Error intencional: Esto no será verdadero