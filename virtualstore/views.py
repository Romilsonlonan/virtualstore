from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, CreateView, FormView
from django.urls import reverse_lazy
from .forms import Checar_PedidoForm, ClienteRegistrarForm, ClienteEntrarForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


#class NavBarView(TemplateView):
#    template_name = 'navbar.html'
    
class HomeView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produto_list'] = Produto.objects.all().order_by("-id")
        return context    
    
# teste
def produtos_por_categoria(request, categoria):
    produtos = Produto.objects.filter(categoria__titulo=categoria)
    return render(request, 'produtos_por_categoria.html', {'produtos': produtos})  
#====================================================================================================
# teste    
from .models import Categoria

def criar_atualizar_categorias(request):
    categorias = [
        {'titulo': 'Eletroeletrônicos', 'slug': 'eletroeletronicos', 'img': 'static/img/eletroeletronicos.png'},
        {'titulo': 'Móveis', 'slug': 'moveis', 'img': 'static/img/moveis.jpg'},
        {'titulo': 'Saúde', 'slug': 'saude', 'img': 'static/img/saude.jpeg'},
        {'titulo': 'Vestuário', 'slug': 'vestuario', 'img': 'static/img/vestuario.jpg'},
        {'titulo': 'Esportes', 'slug': 'esportes', 'img': 'static/img/esportes.jpg'},
    ]

    for categoria_info in categorias:
        categoria, created = Categoria.objects.get_or_create(
            titulo=categoria_info['titulo'],
            slug=categoria_info['slug']
        )

        # Atualiza a imagem da categoria, caso ela exista
        if not created:
            categoria.imagem_categoria = categoria_info['img']
            categoria.save()

    return render(request, 'home.html')  

#=============================================================================================  
class TodosProdutosView(TemplateView):
    template_name = 'todosprodutos.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todoscategorias'] = Categoria.objects.all()
        return context
 
class ProdutoDetalheView(TemplateView):
    template_name = 'produtodetalhe.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        produto = Produto.objects.get(slug=url_slug)
        produto.visualizacao +=1
        produto.save()
        context['produto'] = produto
        return context 
    
     
class AddCarrinhoView(TemplateView):
    template_name = 'addprocarrinho.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produto_id = self.kwargs['pro_id']
        produto_obj = Produto.objects.get(id=produto_id)
        carrinho_id = self.request.session.get('carrinho_id', None)
        
        if carrinho_id:
            carrinho_obj = Carrinho.objects.get(id=carrinho_id)
            produto_no_carrinho = carrinho_obj.carrinhoproduto_set.filter(produto=produto_obj)
            
            if produto_no_carrinho.exists():
                carrinhoproduto=produto_no_carrinho.last()
                carrinhoproduto.quantidade += 1
                carrinhoproduto.subtotal += produto_obj.venda
                carrinhoproduto.save()
                carrinho_obj.total += produto_obj.venda
                carrinho_obj.save()
                
            else:
                carrinhoproduto = CarrinhoProduto.objects.create(
                carrinho = carrinho_obj,
                produto = produto_obj,    
                avaliacao = produto_obj.venda,
                quantidade = 1,  
                subtotal = produto_obj.venda
            )
                carrinho_obj.total += produto_obj.venda
                carrinho_obj.save()
                   
        else:
            carrinho_obj = Carrinho.objects.create(total=0)    
            self.request.session['carrinho_id']=carrinho_obj.id
            carrinhoproduto = CarrinhoProduto.objects.create(
                carrinho = carrinho_obj,
                produto = produto_obj,    
                avaliacao = produto_obj.venda,
                quantidade = 1,  
                subtotal = produto_obj.venda
            )
            carrinho_obj.total += produto_obj.venda
            carrinho_obj.save()
        return context
   
class MeuCarrinhoView(TemplateView):
    template_name = 'meucarrinho.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrinho_id = self.request.session.get('carrinho_id', None)
        
        if carrinho_id:
            carrinho = Carrinho.objects.get(id=carrinho_id)
        else:
            carrinho = None
        context['carrinho'] = carrinho
        return context   

                
class ManipularCarrinhoView(View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs['cp_id']
        acao = request.GET.get('acao')
        cp_obj = CarrinhoProduto.objects.get(id=cp_id)
        carrinho_obj = cp_obj.carrinho 
        
        if acao =="inc":
            cp_obj.quantidade +=1
            cp_obj.subtotal += cp_obj.avaliacao
            cp_obj.save()
            carrinho_obj.total += cp_obj.avaliacao
            carrinho_obj.save()
            
        elif acao =="dcr":
            cp_obj.quantidade -=1
            cp_obj.subtotal -= cp_obj.avaliacao
            cp_obj.save()
            carrinho_obj.total -= cp_obj.avaliacao
            carrinho_obj.save()
            if cp_obj.quantidade == 0:
                cp_obj.delete()
                
        elif acao =="rmv":
            carrinho_obj.total = cp_obj.subtotal
            carrinho_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("virtualstore:meucarrinho")


class LimparCarrinhoView(View):
    def get(self, request, *args, **kwargs):
        carrinho_id = request.session.get('carrinho_id', None)
        
        if carrinho_id:
            carrinho = Carrinho.objects.get(id=carrinho_id)
            carrinho.carrinhoproduto_set.all().delete()
            carrinho.total = 0
            carrinho.save()
        return redirect('virtualstore:meucarrinho')   
    
class CheckoutView(CreateView):
    template_name = 'processar.html'
    form_class = Checar_PedidoForm
    success_url = reverse_lazy("lojavirtual:home")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrinho_id = self.request.session.get('carrinho_id',None)
        if carrinho_id:
            carrinho_obj = Carrinho.objects.get(id=carrinho_id)
        else:
            carrinho_obj = None
        context['carrinho'] = carrinho_obj    
        return context
  
        

   


class ClienteSairView(View):
    def pegar (self,request):
        logout(request)
        return redirect("virtualstore:home")
    
    
class ClienteEntrarView(FormView):
    template_name = 'clienteentrar.html'

class ClienteRegistrarView(CreateView):
    template_name = 'clienteregistrar.html'    
        
class SobreView(TemplateView):
    template_name = 'sobre.html'
    
class ContatoView(TemplateView):
    template_name = 'contato.html'   
