from django.urls import path
from .views import *
#from .views import ckeditor_upload

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
    path("perfil/", ClientePerfilView.as_view(), name="clienteperfil"),
    path("perfil/pedido-<int:pk>/", ClientePedidoDetalheView.as_view(), name="clientepedidodetalhe"), 
    
    path("admin-login/", AdminLoginView.as_view(), name="adminlogin"),
    path("admin-home/", AdminHomeView.as_view(), name="adminhome"),
    path("admin-pedido/<int:pk>/", AdminPedidoDetalheView.as_view(), name="adminpedidodetalhe"), 
    path("admin-todos-pedidos/", AdminPedidoListaView.as_view(), name="adminpedidolista"), 
    path("admin/pedido-<int:pk>-mudar/", AdminPedidoMudarStatusView.as_view(), name="adminpedidomudar"), 
    
    path("pesquisar/", PesquisarView.as_view(), name="pesquisar"),
    path('post/<int:post_id>/', PostViews.as_view(), name='post'),
    path('detalhe-post/<int:post_id>/', DetalhePostViews.as_view(), name='detalhe_post'),
   # path('ckeditor/upload/', ckeditor_upload, name='ckeditor_upload'),
    path('blog/', BlogViews.as_view(), name='blog'),
]