from django.contrib import admin
from .models import Usuario, Transportador, Regiao_CG, Bairros_CG

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome_usuario', 'telefone', 'logradouro', 'nr_porta', 'bairro', 'cep', 'latitude', 'longitude', 'criado', 'modificado')
    search_fields = ('nome_usuario', 'telefone', 'logradouro', 'bairro', 'cep')
    list_filter = ('bairro',)
    readonly_fields = ('criado', 'modificado')

@admin.register(Transportador)
class TransportadorAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'telefone_fixo', 'telefone_celular', 'email','logradouro','nr_porta', 'bairro', 'regiao', 'is_ativo', 'modificado')
    search_fields = ('nome_fantasia', 'telefone_fixo', 'telefone_celular', 'email', 'bairro', 'cep')
    list_filter = ('regiao', 'is_ativo')
    readonly_fields = ('criado', 'modificado')

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
