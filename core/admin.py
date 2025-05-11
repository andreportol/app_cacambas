from django.contrib import admin
from .models import Usuario, Transportador, Regiao_CG, Bairros_CG,Produto, TransportadorProduto, Pedido

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome_usuario', 'telefone', 'logradouro', 'nr_porta', 'bairro', 'cep', 'criado', 'modificado')
    search_fields = ('nome_usuario', 'telefone', 'logradouro', 'bairro', 'cep')
    list_filter = ('bairro',)
    readonly_fields = ('criado', 'modificado')

# Inline para a relação TransportadorProduto
class TransportadorProdutoInline(admin.TabularInline):
    model = TransportadorProduto
    extra = 1  # Define o número de linhas adicionais para edição

@admin.register(Transportador)
class TransportadorAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'telefone_fixo', 'telefone_celular', 'logradouro','nr_porta', 'bairro', 'regiao','mostrar_regioes_trabalho', 'is_ativo', 'modificado')
    search_fields = ('nome_fantasia', 'telefone_fixo', 'telefone_celular', 'email', 'bairro', 'cep')
    list_filter = ('regiao', 'is_ativo')
    readonly_fields = ('criado', 'modificado')
    inlines = [TransportadorProdutoInline]  # Adiciona o inline para gerenciar os produtos relacionados
    ordering=['-is_ativo','nome_fantasia']  # Na tela admin mostra primeiro os ativos e em ordem alfabética
    def mostrar_regioes_trabalho(self, obj):
        return ", ".join([str(regiao) for regiao in obj.regioes_trabalho.all()])

    
    mostrar_regioes_trabalho.short_description = 'Regiões de Trabalho'

# Registro da classe Produto
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    # ordena por ordem alfabética
    ordering = ['nome']

@admin.register(Regiao_CG)
class Regiao_CGAdmin(admin.ModelAdmin):
    list_display = ('nome_regiao',)
    search_fields = ('nome_regiao',)
    ordering = ['nome_regiao']
    #filter_horizontal = ('nome_transportador',)

@admin.register(Bairros_CG)
class Bairros_CGAdmin(admin.ModelAdmin):
    list_display = ('nome_bairro','nome_regiao_regioes')
    search_fields = ('nome_bairro','nome_regiao_regioes')
    list_filter = ('nome_regiao_regioes',)
    # ordena por ordem alfabética
    ordering = ['nome_bairro']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        'numero_pedido','status_pedido', 'nome_cliente', 'telefone_cliente',
        'transportador', 'produto', 'quantidade_desejada',
        'data_inicio', 'data_retirada', 'preco','recebido', 'observacao'
    )
    list_filter = ('status_pedido', 'data_inicio', 'data_retirada', 'transportador','recebido')
    search_fields = ('numero_pedido', 'nome_cliente', 'telefone_cliente', 'transportador__nome_fantasia')
    readonly_fields = ('numero_pedido',)

    fieldsets = (
        ('Identificação', {
            'fields': ('numero_pedido', 'status_pedido')
        }),
        ('Dados do Cliente', {
            'fields': ('nome_cliente', 'telefone_cliente')
        }),
        ('Endereço da Obra', {
            'fields': ('logradouro', 'num_porta', 'bairro', 'cidade')
        }),
        ('Dados do Pedido', {
            'fields': ('transportador', 'produto', 'tipo_entulho', 'quantidade_desejada', 'preco')
        }),
        ('Datas', {
            'fields': ('data_inicio', 'data_retirada')
        }),
        ('Observação', {
            'fields': ('observacao',)
        }),
    )
