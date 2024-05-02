from django import forms
# esta com erro no django.forms add provisoriamente o from django import forms acima
from django.forms import ModelForm, TextInput, EmailInput
from .models import PedidoOrdem, Cliente
from django.contrib.auth.models import User

class Checar_PedidoForm(forms.ModelForm):
    class Meta:
        model = PedidoOrdem
        fields = ["ordenado_por", "endereco_envio", "telefone", "email"]
        widgets = {
            'ordenado_por': forms.TextInput(attrs={
                'class': 'form-control placeholder-style',
                'placeholder': 'Pedido Por',
            }),
            'endereco_envio': forms.TextInput(attrs={
                'class': 'form-control placeholder-style',
                'placeholder': 'Endereço de Envio',
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control placeholder-style',
                'placeholder': 'Telefone',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control placeholder-style',
                'placeholder': 'Email',
            }),
        }
        
 
class ClienteRegistrarForm(forms.ModelForm):
    
    username = forms.CharField(widget=forms.TextInput())
    
    password = forms.CharField(widget=forms.PasswordInput())
    
    email = forms.CharField(widget=forms.EmailInput())
    
        
    class Meta:
        model = Cliente
        fields = ["username", "password", "email", "nome_completo", "endereco"]
        
    def clean_username(self):
        nome = self.cleaned_data.get('username')
        if User.objects.filter(username=nome).exists():
            raise forms.ValidationError("Este cliente já existe")   
        return nome 

class ClienteEntrarForm(forms.Form):
    
    username = forms.CharField(widget=forms.TextInput())
    
    password = forms.CharField(widget=forms.PasswordInput())
    
    email = forms.CharField(widget=forms.EmailInput())
    
  