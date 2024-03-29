from django.contrib import admin
from .models import Cliente, Categoria, Produto, Carrinho, CarrinhoProduto, PedidoOrdem

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'imagem_categoria']  # Adicione 'imagem_categoria' à lista de campos exibidos
    search_fields = ['titulo']  # Permitir pesquisa por título
    prepopulated_fields = {'slug': ('titulo',)}  # Preencher automaticamente o campo de slug com base no título

# Verificar se a Categoria ainda não está registrada antes de registrar
if not admin.site.is_registered(Categoria):
    admin.site.register(Categoria, CategoriaAdmin)

admin.site.register([Cliente, Produto, Carrinho, CarrinhoProduto, PedidoOrdem])

