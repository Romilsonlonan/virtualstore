from django.test import TestCase
from django.urls import reverse

class CategoriaViewTest(TestCase):
    def test_lista_categorias(self):
        response = self.client.get(reverse('todos-produtos'))
        self.assertEqual(response.status_code, 200)
        # Adicione mais asserções conforme necessário
