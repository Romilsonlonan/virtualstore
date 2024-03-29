from django.urls import path
from .views import *
    

app_name = 'virtualstore'
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("sobre/", SobreView.as_view(), name="sobre"),
    path("contato/", ContatoView.as_view(), name="contato"),
    path("todos-produtos/", TodosProdutosView.as_view(), name="todos-produtos"),
    path("produto/<slug:slug>/", ProdutoDetalheView.as_view(), name="produto-detalhe"),
    path('categoria/<str:categoria>/', produtos_por_categoria, name='categoria'),
    path("addcarrinho-<int:pro_id>/", AddCarrinhoView.as_view(), name="addcarrinho"),
    path("meu-carrinho/", MeuCarrinhoView.as_view(), name="meucarrinho"),
    path("manipular-carrinho/<int:cp_id>/", ManipularCarrinhoView.as_view(), name="manipularcarrinho"),
    path("limpar-carrinho/", LimparCarrinhoView.as_view(), name="limparcarrinho"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("registrar/", ClienteRegistrarView.as_view(), name="clienteregistrar"),
    path("sair/", ClienteSairView.as_view(), name="clientesair"),
    path("entrar/", ClienteEntrarView.as_view(), name="clienteentrar"),
]