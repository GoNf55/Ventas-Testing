from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class LoginIntegrationTests(TestCase):
       
    def setUp(self):
        # Crear un usuario para las pruebas de login
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword123'
        )
        self.login_url = reverse('login')  # Cambia 'login' por el nombre de la URL de tu vista de login

    def test_login_successful(self):
        # Simular un POST a la vista de login con credenciales correctas
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        # Verificar que el usuario fue autenticado y redirigido correctamente
        self.assertEqual(response.status_code, 302)  # Asumiendo que redirige en caso de éxito
        self.assertRedirects(response, reverse('home'))  # Ajustar a tu URL de redirección post-login
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_password(self):
        # Simular un POST a la vista de login con un password incorrecto
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        # Verificar que el login no fue exitoso
        self.assertEqual(response.status_code, 200)  # La misma página de login se renderiza nuevamente
        self.assertIn(b'Por favor, introduzca un nombre de usuario y clave correctos.', response.content)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_user_does_not_exist(self):
        # Intentar login con un usuario que no existe
        response = self.client.post(self.login_url, {
            'username': 'nouser',
            'password': 'anypassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Por favor, introduzca un nombre de usuario y clave correctos.', response.content)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


