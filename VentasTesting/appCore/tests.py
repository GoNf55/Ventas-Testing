from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class LoginTest(TestCase):
    
    def setUp(self):
        # Crear un usuario para pruebas
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='testuser'
        )
        self.login_url = reverse('login')
        self.home_url = reverse('home')

    def test_login_success(self):
        # Verificar que un usuario con credenciales correctas puede iniciar sesión exitosamente.
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertRedirects(response, self.home_url)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_failure(self):
        # Verificar que un usuario con credenciales incorrectas recibe un mensaje de error y no puede iniciar sesión.
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Por favor, introduzca un nombre de usuario y clave correctos. Observe que ambos campos pueden ser sensibles a mayúsculas.")
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_redirect_after_login(self):
        # Verificar que, después de iniciar sesión, el usuario es redirigido a la página de inicio o la página correcta.
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertRedirects(response, self.home_url)

    def test_protected_view_without_login(self):
        #Verificar que los usuarios que no han iniciado sesión no pueden acceder a páginas protegidas.
        response = self.client.get(self.home_url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'{self.login_url}?next={self.home_url}')

    def test_access_protected_view_after_login(self):
        # Verificar que un usuario puede acceder a una página protegida después de iniciar sesión.
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bienvenido testuser !")
