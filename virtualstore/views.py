from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, CreateView, FormView
from django.urls import reverse_lazy
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

class HomeView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produto_list'] = Produto.objects.all().order_by("-id")
        return context
    
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
  
        return context
     
class AddCarrinhoView(TemplateView):
    template_name = 'addprocarrinho.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
   
class MeuCarrinhoView(TemplateView):
    template_name = 'meucarrinho.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrinho_id = self.request.session.get('carrinho_id', None)
       
        return context   

                
class ManipularCarrinhoView(View):
    def get(self, request, *args, **kwargs):
   
        return redirect("lojavirtual:meucarrinho")


class LimparCarrinhoView(View):
    def get(self, request, *args, **kwargs):
        carrinho_id = request.session.get('carrinho_id', None)
    
        return redirect('lojavirtual:meucarrinho')   
    
class CheckoutView(CreateView):
    template_name = 'processar.html'
  
        

   


class ClienteSairView(View):
    def pegar (self,request):
        logout(request)
        return redirect("lojavirtual:home")
    
    
class ClienteEntrarView(FormView):
    template_name = 'clienteentrar.html'

    
        
class SobreView(TemplateView):
    template_name = 'sobre.html'
    
class ContatoView(TemplateView):
    template_name = 'contato.html'   
