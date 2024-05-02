from django.contrib import admin
from .models import Admin, Cliente, Categoria, Produto, Carrinho, CarrinhoProduto, PedidoOrdem, Post

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'imagem_categoria']  
    search_fields = ['titulo']  
    prepopulated_fields = {'slug': ('titulo',)}  

class PostAdmin(admin.ModelAdmin):
    list_display = ['titulo_post', 'autor', 'data_publicacao', 'imagem_post']
    search_fields = ['titulo_post', 'conteudo']
    list_filter = ['data_publicacao']
    date_hierarchy = 'data_publicacao'
    ordering = ['-data_publicacao']
    
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Produto)
admin.site.register(Carrinho)
admin.site.register(CarrinhoProduto)
admin.site.register(PedidoOrdem)

# Registre o modelo Post associado ao PostAdmin
admin.site.register(Post)

