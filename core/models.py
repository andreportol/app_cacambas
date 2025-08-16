from django.db import models 
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class Base(models.Model):
    criado = models.DateTimeField('Criação', auto_now_add=True)
    modificado = models.DateTimeField('Atualização', auto_now=True)
    
    class Meta:
        abstract = True

class Usuario(Base):
    nome_usuario = models.CharField(verbose_name='Nome de usuário', max_length=150)
    telefone = models.CharField(verbose_name='Telefone', max_length=10)
    logradouro = models.CharField(verbose_name='Logradouro', max_length=200)
    nr_porta = models.CharField(verbose_name='Número de porta', max_length=5)
    cep = models.CharField(verbose_name='CEP', max_length=9)
    bairro = models.CharField(verbose_name='Bairro', max_length=100)
        
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return self.nome_usuario

class Regiao_CG(models.Model):
    REGIAO_CHOICES = [
        ('SEGREDO','SEGREDO'),  
        ('PROSA','PROSA'),
        ('CENTRO','CENTRO'),
        ('IMBIRUSSU','IMBIRUSSU'),
        ('LAGOA','LAGOA'),
        ('ANHANDUIZINHO','ANHANDUIZINHO'),
        ('BANDEIRA','BANDEIRA'),
    ]
    nome_regiao = models.CharField(verbose_name='Região', choices=REGIAO_CHOICES, max_length=13, unique=True)  
        
    class Meta:
        verbose_name = 'Região'
        verbose_name_plural = 'Regiões'
    
    def __str__(self):
        return self.nome_regiao

class Bairros_CG(models.Model):
    nome_bairro = models.CharField(verbose_name='Bairro', max_length=150, unique=True)
    nome_regiao_regioes = models.ForeignKey(Regiao_CG,to_field='nome_regiao',  verbose_name='Nome Região', on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = 'Bairro'
        verbose_name_plural = 'Bairros'
    
    def __str__(self):
        return self.nome_bairro

class Produto(models.Model):
    NOME_PRODUTO_CHOICES = [
        ('cacamba_2m', 'Caçamba 2m³'),
        ('cacamba_3m', 'Caçamba 3m³'),
        ('cacamba_4m', 'Caçamba 4m³'),
        ('caminhao_5m', 'Caminhão 5m³'),
        ('caminhao_12m', 'Caminhão 12m³'),
        ('caminhao_25m', 'Caminhão 25m³'),
        ('roll_roll_25m', 'Roll Roll 25m³'),
        ('roll_roll_32m', 'Roll Roll 32m³'),
    ]
    nome = models.CharField(max_length=50, choices=NOME_PRODUTO_CHOICES, unique=True)

    def __str__(self):
        return self.get_nome_display()

class Transportador(Base):
    # Contato
    nome_fantasia = models.CharField(verbose_name='Nome transportador', max_length=150, unique=True)
    cnpj = models.CharField(verbose_name='CNPJ', max_length=18, unique=True, blank=True, null=True)
    telefone_fixo = models.CharField(verbose_name='Telefone Fixo', max_length=16, blank=True)
    telefone_extra = models.CharField(verbose_name='Telefone Extra', max_length=16, blank=True)
    telefone_celular = models.CharField(verbose_name='Telefone celular', max_length=16, blank=True)
    email = models.EmailField(verbose_name='E-mail', max_length=150, blank=False)
    senha = models.CharField(max_length=128, blank=True, null=True)
    # Endereço
    logradouro = models.CharField(verbose_name='Logradouro', max_length=200)
    nr_porta = models.CharField(verbose_name='Número de porta', max_length=5)
    cep = models.CharField(verbose_name='CEP', max_length=9)
    bairro = models.CharField(verbose_name='Bairro', max_length=100)
    REGIAO_CHOICES = [
        ('SEGREDO','SEGREDO'),  
        ('PROSA','PROSA'),
        ('CENTRO','CENTRO'),
        ('IMBIRUSSU','IMBIRUSSU'),
        ('LAGOA','LAGOA'),
        ('ANHANDUIZINHO','ANHANDUIZINHO'),
        ('BANDEIRA','BANDEIRA'),
    ]
    regiao = models.CharField(verbose_name='Região', max_length=13, choices=REGIAO_CHOICES)  
    #latitude = models.CharField(verbose_name='Latitude', max_length=10)
    #longitude = models.CharField(verbose_name='Longitude', max_length=10)
    # Status
    is_ativo = models.BooleanField(verbose_name='Ativo',default=False)
    # Serviços
    regioes_trabalho = models.ManyToManyField(Regiao_CG, verbose_name='Regiões de Trabalho')
    #produtos
    produtos = models.ManyToManyField(Produto, through='TransportadorProduto')
    
    class Meta:
        verbose_name = 'Transportador'
        verbose_name_plural = 'Transportadores'
        ordering = ['is_ativo', 'nome_fantasia']   
    def set_senha(self, raw_password):
        self.senha = make_password(raw_password)

    def check_senha(self, raw_password):
        return check_password(raw_password, self.senha)

    def __str__(self):
        return self.nome_fantasia

# Uma classe intermediaria que serve para que cada transportador tenha um preço distinto por produto;
class TransportadorProduto(models.Model):
    #Transportador entre aspas significa que a classe Transportadora pode não ter sido criada ainda, ou seja, pode ser criada depois dessa classe.
    transportador = models.ForeignKey('Transportador', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    qtd_produto = models.IntegerField(verbose_name='Quantidade do produto', null=True)

    def __str__(self):
        return f"{self.transportador.nome_fantasia} - {self.produto.get_nome_display()} - R${self.preco}"


class Pedido(Base):
    numero_pedido = models.IntegerField(verbose_name="Número do Pedido", unique=True, editable=False)

    STATUS_CHOICES = [
        ('NOVO', 'NOVO'),
        ('PENDENTE', 'PENDENTE'),
        ('ATENDIDO', 'ATENDIDO'),
        ('FINALIZADO', 'FINALIZADO'),
        ('CANCELADO', 'CANCELADO'),
    ]
    status_pedido = models.CharField(verbose_name='Status', choices=STATUS_CHOICES, max_length=10, default='NOVO')

    #usuario = models.ForeignKey(Usuario, verbose_name="Usuário", on_delete=models.CASCADE)
    transportador = models.ForeignKey('Transportador', verbose_name="Transportador", on_delete=models.CASCADE)
    produto = models.ForeignKey('Produto', verbose_name="Produto", on_delete=models.CASCADE)

    tipo_entulho = models.CharField(max_length=20, verbose_name="Tipo de Entulho")
    quantidade_desejada = models.IntegerField(verbose_name="Quantidade Desejada")

    logradouro = models.CharField(max_length=255)
    num_porta = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100, default='Não informado')
    cidade = models.CharField(max_length=100)

    data_inicio = models.DateField(verbose_name="Data de Início")
    data_retirada = models.DateField(verbose_name="Data de Retirada")

    nome_cliente = models.CharField(max_length=255)
    telefone_cliente = models.CharField(max_length=20)
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    recebido = models.BooleanField(verbose_name= "Recebido", default=False)
    observacao = models.TextField(verbose_name='Obs:', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f'Pedido #{self.numero_pedido} - {self.nome_cliente}'

    def save(self, *args, **kwargs):
        if not self.numero_pedido:
            ultimo_pedido = Pedido.objects.all().order_by('-numero_pedido').first()
            self.numero_pedido = (ultimo_pedido.numero_pedido + 1) if ultimo_pedido else 1
        super().save(*args, **kwargs)


