from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.apps import apps

class ViewTestCase(TestCase):
    def setUp(self):
        # Criando um usuário
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='12345')

    def test_all_views(self):
        # Logando como o usuário criado
        self.client.login(username='testuser', password='12345')
        
        # Obtendo todas as views do projeto
        all_views = []
        for app_config in apps.get_app_configs():
            for url_pattern in app_config.get_models():
                all_views.append(url_pattern)
        
        # Testando cada view
        for view in all_views:
            try:
                url = reverse(view)
                response = self.client.get(url)
                self.assertIsNotNone(response)
                self.assertEqual(response.status_code, 200)  # Verificando se o status code é 200 (OK)
            except:
                print(f"Acesso à view {view} falhou.")
