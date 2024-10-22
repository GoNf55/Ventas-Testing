from django.test import TestCase
from django.urls import reverse
from clientes.models import Cliente

class ClienteIntegrationTests(TestCase):
    
    def setUp(self):
        # Crear datos iniciales para las pruebas
        self.cliente1 = Cliente.objects.create(
            nombre="Juan", apellido="Perez", email="juan.perez@example.com", telefono="123456789", dni="12345678"
        )
        self.cliente2 = Cliente.objects.create(
            nombre="Maria", apellido="Gomez", email="maria.gomez@example.com", telefono="987654321", dni="87654321"
        )

    def test_listar_clientes(self):
        # Verificar que la vista de clientes se carga correctamente
        response = self.client.get(reverse('clientes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clientes/clientes.html')
        self.assertContains(response, self.cliente1.nombre)
        self.assertContains(response, self.cliente2.nombre)

    def test_agregar_cliente(self):
        # Simular agregar un cliente
        response = self.client.post(reverse('addcliente'), {
            'nombre': 'Carlos',
            'apellido': 'Ramirez',
            'email': 'carlos.ramirez@example.com',
            'telefono': '1122334455',
            'dni': '34567890'
        })
        # Verificar que se redirige correctamente
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('clientes'))
        
        # Comprobar que el cliente fue agregado
        self.assertTrue(Cliente.objects.filter(nombre='Carlos', apellido='Ramirez').exists())

    def test_modificar_cliente(self):
        # Simular modificación de un cliente existente
        response = self.client.post(reverse('modcliente', args=[self.cliente1.id_cliente]), {
            'nombre': 'Juan',
            'apellido': 'Martinez',  # Cambiado de Perez a Martinez
            'email': 'juan.martinez@example.com',
            'telefono': '123456789',
            'dni': '12345678'
        })
        # Verificar que se redirige correctamente
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('clientes'))
        
        # Comprobar que los cambios fueron guardados
        self.cliente1.refresh_from_db()
        self.assertEqual(self.cliente1.apellido, 'Martinez')
        self.assertEqual(self.cliente1.email, 'juan.martinez@example.com')

    def test_eliminar_cliente(self):
        # Simular eliminación de un cliente
        response = self.client.post(reverse('delcliente', args=[self.cliente1.id_cliente]))
        # Verificar que se redirige correctamente
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('clientes'))
        
        # Comprobar que el cliente fue eliminado
        self.assertFalse(Cliente.objects.filter(id_cliente=self.cliente1.id_cliente).exists())
