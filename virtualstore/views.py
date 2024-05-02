from urllib import request
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from django.urls import reverse_lazy
from .forms import Checar_PedidoForm, ClienteRegistrarForm, ClienteEntrarForm
from .models import*
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.db.models import Q


#class NavBarView(TemplateView):
#    template_name = 'navbar.html'

class LojaRKOfertas(object):
    def dispatch(self, request, *args, **kwargs):
        carrinho_id = request.session.get("carrinho_id")
       
        return super().dispatch(request, *args, **kwargs)
    
class HomeView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todos_produtos_pg = Produto.objects.all().order_by("-id")
        paginacao = Paginator(todos_produtos_pg,3)
        numero_paginas = self.request.GET.get("pagina")
        context['lista_produto'] = Produto.objects.all().order_by("-id")
        context['latest_news'] = Post.objects.filter(tipo_post='news').order_by('-data_publicacao')[:4]
        #context['latest_offers'] = Post.objects.filter(post_type='offer').order_by('-published_date')[:4]
        #context['latest_others'] = Post.objects.filter(post_type='other').order_by('-published_date')[:4]
        return context    

class BlogViews(View):
    def get(self, request):
        posts = Post.objects.all()  # Obtém todos os posts do banco de dados
        context = {'posts': posts}  # Cria o contexto com os posts
        return render(request, 'blog.html', context)

class PostViews(View):
    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        return render(request, 'home.html', {'post': post})
   
class DetalhePostViews(View):
    def get(self, request, post_id):
        detalhe_post = Post.objects.get(id=post_id)

        return render(request, 'home.html', {'detalhe_post': detalhe_post})
 

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
    success_url = reverse_lazy("virtualstore:home")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrinho_id = self.request.session.get('carrinho_id',None)
        if carrinho_id:
            carrinho_obj = Carrinho.objects.get(id=carrinho_id)
        else:
            carrinho_obj = None
        context['carrinho'] = carrinho_obj    
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.cliente: # verificar errp em aulas 12 a 14
        #if request.user.is_authenticated and hasattr(request.user, 'cliente'): # verificar errp em aulas 12 a 14
            pass
        else:
            return redirect("/entrar/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs) # verificar errp em aulas 12 a 14


    '''
    "form_valid" é um método usado em classes de visualização baseadas em 
    formulários (como FormView, CreateView, UpdateView, entre outras) para 
    lidar com o processamento de um formulário quando ele é válido.
    '''
    def form_valid(self, form):
        carrinho_id = self.request.session.get('carrinho_id')
        if carrinho_id:
            carrinho_obj = Carrinho.objects.get(id=carrinho_id)
            form.instance.carrinho = carrinho_obj
            form.instance.subtotal = carrinho_obj.total
            form.instance.desconto = 0
            form.instance.total = carrinho_obj.total
            #Ao enviar o pedido 
            form.instance.pedido_status = "Pedido Recebido"
            #deletando o carrinho após relizar a compra com sucesso automaticamente
            del self.request.session['carrinho_id']
        else:
            return redirect("virtualstore:home")
        return super().form_valid(form)   

class ClienteRegistrarView(CreateView):
    template_name = 'clienteregistrar.html'
    form_class = ClienteRegistrarForm
    success_url = reverse_lazy("virtualstore:home")
    
    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username,email,password)
        
        form.instance.user = user
        #Adicionar mensagem para cliente logado
        login(self.request, user)
        return super().form_valid(form)


class ClienteSairView(View):
    def pegar (self,request):
        logout(request)
        return redirect("virtualstore:home")
    
    
class ClienteEntrarView(FormView):
    template_name = 'clienteentrar.html'
    form_class = ClienteSairView
    success_url = reverse_lazy("virtualstore:home")
    
    def form_valid(self, form):
        nome = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=nome,password=pword)
        if usr is not None and Cliente.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class,"error": "Erro ao logar"})    
        return super().form_valid(form)
    
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
             return self.success_url            
        
class ClientePerfilView(TemplateView):
    template_name = "clienteperfil.html"
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated and Cliente.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/entrar/?next=/perfil/")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        cliente = self.request.user.cliente
        context['cliente'] = cliente
        
        pedidos = PedidoOrdem.objects.filter(carrinho__cliente=cliente).order_by('-id')
        context['pedidos'] = pedidos  
        return context
        
class ClientePedidoDetalheView (DetailView):
    template_name = 'clientepedidodetalhe.html'  
    model = PedidoOrdem
    context_object_name = "pedido_obj"    
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated and Cliente.objects.filter(user=request.user).exists():
            ordem_id = self.kwargs["pk"]
            pedido = PedidoOrdem.objects.get(id=ordem_id)
            if request.user.cliente != pedido.carrinho.cliente:
                return redirect("virtualstore:clienteperfil")
        else:
            return redirect("/entrar/?next=/perfil/")
        return super().dispatch(request, *args, **kwargs)  
      
class AdminLoginView(FormView):
    template_name = "admin_paginas/adminlogin.html"
    form_class = ClienteEntrarForm
    success_url = reverse_lazy("virtualstore:adminhome")
    
    def form_valid(self, form):
        nome = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=nome,password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class,"error": "Erro ao logar"})    
        return super().form_valid(form)

###############################################################################################
# Classe criada para leitura de código
class AdminRequireMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("admin_paginas/admin-login/")
        return super().dispatch(request, *args, **kwargs)         

# ESTA COM ERRO - VERIFICAR URL "admin-home" SE FOI CRIADA 
###############################################################################################
class AdminHomeView(AdminRequireMixin, TemplateView):
    template_name = "admin_paginas/adminhome.html"
   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["PedidosPendentes"] = PedidoOrdem.objects.filter(pedido_status="Pedido Recebido").order_by("-id")
        return context
    
class AdminPedidoDetalheView(AdminRequireMixin, DetailView):
    template_name = "admin_paginas/adminpedidodetalhe.html"
    
    model = PedidoOrdem
        
    context_object_name = "pedido_obj"
    
    def get_context_data(self, **kwargs):         
        context = super().get_context_data(**kwargs)
        context["todosstatus"]= PEDIDO_STATUS
        
        return context
    
    
class AdminPedidoListaView(AdminRequireMixin, ListView):
    template_name = "admin_paginas/adminpedidolista.html"
    
    queryset = PedidoOrdem.objects.all().order_by("-id")
        
    context_object_name = "todospedidos"  
    

class AdminPedidoMudarStatusView(AdminRequireMixin, View):
    
    def post(self, request, *args, **kwargs):
        pedido_id = self.kwargs["pk"]
        pedido_obj = PedidoOrdem.objects.get(id=pedido_id)
        novo_status = request.get('status')
        
        PedidoOrdem.pedido_status = novo_status
        pedido_obj.save()  
        
        return redirect(reverse_lazy("virtualstore:adminpedidodetalhe", kwargs={"pk" : self.kwargs["pk"]}))
        
                
class PesquisarView(TemplateView):
    template_name = "pesquisar.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Produto.objects.filter(Q(titulo__icontains=kw) | Q(descricao__icontains=kw) | Q(retorno_devolucao__icontains=kw))
        context["results"] = results 
        if results.exists():
            context["results"] = results
        else:
            context["mensagem_alerta"] = "Nenhum resultado encontrado para a pesquisa: '{}'".format(kw)
        
        return context 



class SobreView(TemplateView):
    template_name = 'sobre.html'
    
class ContatoView(TemplateView):
    template_name = 'contato.html'    