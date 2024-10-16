from django.contrib import admin
from .models import Usuario, Transportador, Regiao_CG, Bairros_CG,Produto, TransportadorProduto

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome_usuario', 'telefone', 'logradouro', 'nr_porta', 'bairro', 'cep', 'latitude', 'longitude', 'criado', 'modificado')
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

    def mostrar_regioes_trabalho(self, obj):
        return ", ".join([str(regiao) for regiao in obj.regioes_trabalho.all()])

    
    mostrar_regioes_trabalho.short_description = 'Regiões de Trabalho'

# Registro da classe Produto
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Regiao_CG)
class Regiao_CGAdmin(admin.ModelAdmin):
    list_display = ('nome_regiao',)
    search_fields = ('nome_regiao',)
    ordering = ['nome_regiao']
    #filter_horizontal = ('nome_transportador',)

@admin.register(Bairros_CG)
class Bairros_CGAdmin(admin.ModelAdmin):
    list_display = ('nome_regiao_regioes','nome_bairro')
    search_fields = ('nome_bairro',)
    list_filter = ('nome_regiao_regioes',)
    # ordena por ordem alfabética
    ordering = ['nome_regiao_regioes']
