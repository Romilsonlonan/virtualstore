from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 
#from ckeditor.fields import RichTextField
#from ckeditor_uploader.fields import RichTextUploadingField


class Admin(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100)
    image = models.ImageField(upload_to="admins")
    tel = models.CharField(max_length=20)
     
    def __str__(self):
        return self.user.username

class Cliente(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200,null=True,blank=True)
    data_on = models.DateField(auto_now_add=True)
     
    def __str__(self):
        return self.nome_completo
    
class Categoria(models.Model):
    titulo = models.CharField(max_length=200)
    imagem_categoria = models.ImageField(upload_to="categorias", blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.titulo
    
    
class Produto(models.Model):
    titulo = models.CharField(max_length=200)
    #garante que o valor armazenado seja um texto simplificado, 
    #composto apenas de letras, números, hífens e sublinhados, sem espaços ou caracteres especiais.
    slug = models.SlugField(unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to="produtos")
    preco_marcado = models.PositiveIntegerField()
    venda = models.PositiveIntegerField()
    descricao = models.TextField()
    garantia = models.CharField(max_length=300, null=True, blank=True)
    retorno_devolucao = models.CharField(max_length=300,null=True, blank=True)
    visualizacao = models.PositiveIntegerField(default=0)    
    
    def __str__(self):
        return self.titulo
    
    
class Carrinho(models.Model):
    cliente = models.ForeignKey(Cliente,on_delete=models.SET_NULL,null=True,blank=True)
    total = models.PositiveIntegerField(default=0)    
    criado_em = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return "Carrinho" + str(self.id)


class CarrinhoProduto(models.Model):
    carrinho = models.ForeignKey(Carrinho,on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto,on_delete=models.CASCADE)    
    avaliacao = models.PositiveIntegerField()
    quantidade = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
#    update = models.DateTimeField(auto_now = True)
#    timestamp = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return "Carrinho" + str(self.carrinho.id) + "CarrinhoProduto: " + str(self.id)
        
PEDIDO_STATUS=(
    ("Pedido Recebido", "Pedido Recebido"),
    ("Pedido Processado", "Pedido Processado"),
    ("Pedido a caminho", "Pedido a caminho"),
    ("Pedido Completado", "Pedido Completado"),
    ("Pedido Cancelado", "Pedido Cancelado"),
)
        
class PedidoOrdem(models.Model):
    carrinho = models.OneToOneField(Carrinho,on_delete=models.CASCADE)
    ordenado_por = models.CharField(max_length=200)
    telefone = models.CharField(max_length=10)
    email = models.EmailField(null=True,blank=True)
    endereco_envio = models.CharField(max_length=200)
    # Não visualizado pelo cliente (instancia criada na views.py)
    subtotal = models.PositiveIntegerField()
    desconto = models.PositiveIntegerField() 
    total = models.PositiveIntegerField()    
    pedido_status = models.CharField(max_length=50,choices=PEDIDO_STATUS)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "PedidoOrdem:" + str(self.id) 
    
    
class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('news', 'Notícia'),
        ('offer', 'Oferta Exclusiva'),
        ('other', 'Outro'),
    ]

    titulo_post = models.CharField(max_length=200)
    sumario = models.TextField(max_length=255)
    conteudo_post = models.TextField() #() sem limites de armazenamento de caracteres
    #sumario = RichTextField(max_length=255)
    #conteudo_post = RichTextUploadingField() 
    autor_post = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    data_criacao = models.DateTimeField(default=timezone.now)
    data_publicacao = models.DateTimeField(blank=True, null=True)
    imagem_post = models.ImageField(upload_to='imagem_post/', blank=True, null=True)  # Campo para o upload da imagem
    compartilhavel = models.BooleanField(default=True)
    comentarios_ativados = models.BooleanField(default=True)
    tipo_post = models.CharField(max_length=10, choices=POST_TYPE_CHOICES, default='other')

    class Meta:
        ordering = ['-data_publicacao']

    def publicar(self):
        self.data_publicacao = timezone.now()
        self.save()

    def __str__(self):
        return self.titulo_post