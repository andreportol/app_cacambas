from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
from django.shortcuts import render
from core.models import Pedido
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

'''
Método decorator para verificar se está logado
caso não esteja, direcionar para tela de login do django
'''
# decorator utilizado para que somente superusuarios acessem o dashboard da empresa
@method_decorator(
    user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/'),
    name='dispatch'
)
class IndexTemplateView(TemplateView):
    template_name = 'index_dashboard.html'
    
@method_decorator(
    user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/'),
    name='dispatch'
)
class TabelaPedidosNovosListView(ListView):
    template_name = 'tabela_pedidos.html'
    model = Pedido
    context_object_name = 'pedidos'
    '''
    O método get_queryset é utilizado para personalizar a 
    consulta do banco de dados. Neste caso, estamos 
    filtrando os objetos Pedido onde o campo status_pedido 
    é igual a 'NOVO'.
    '''
    def get_queryset(self):
        # Filtrando os pedidos com status 'NOVO'
        return Pedido.objects.filter(status_pedido='NOVO').order_by('-id')  
@method_decorator(
    user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/'),
    name='dispatch'
)
class TabelaPedidosPendentesListView(ListView):
    template_name = 'tabela_pedidos.html'
    model = Pedido
    context_object_name = 'pedidos'
    
    def get_queryset(self):
        return Pedido.objects.filter(status_pedido='PENDENTE').order_by('-id')  
@method_decorator(
    user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/'),
    name='dispatch'
)
class TabelaPedidosAtendidosListView(ListView):
    template_name = 'tabela_pedidos.html'
    model = Pedido
    context_object_name = 'pedidos'
    
    def get_queryset(self):
        return Pedido.objects.filter(status_pedido='ATENDIDO').order_by('-id')
@method_decorator(
    user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/'),
    name='dispatch'
)
class TabelaPedidosFinalizadosListView(ListView):
    template_name = 'tabela_pedidos.html'
    model = Pedido
    context_object_name = 'pedidos'
    
    def get_queryset(self):
        return Pedido.objects.filter(status_pedido='FINALIZADO').order_by('-id')
@method_decorator(
    user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/'),
    name='dispatch'
)
class TabelaPedidosCanceladosListView(ListView):
    template_name = 'tabela_pedidos.html'
    model = Pedido
    context_object_name = 'pedidos'
    
    def get_queryset(self):
        return Pedido.objects.filter(status_pedido='CANCELADO').order_by('-id')
@method_decorator(
    user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/'),
    name='dispatch'
)
class TabelaPedidosArquivadosListView(ListView):
    template_name = 'tabela_pedidos.html'
    model = Pedido
    context_object_name = 'pedidos'
    
    def get_queryset(self):
        return Pedido.objects.filter(status_pedido='ARQUIVADOS').order_by('-id')

# variável global -> necessário para atualizar a tabela de novos pedidos
contador_old = 0

# Método utilizado para os mostradores
@staff_member_required(login_url='/admin/login/')
def dados_pedidos(request):
    global contador_old
    dados = {
        'novos': Pedido.objects.filter(status_pedido='NOVO').count(),
        'pendentes': Pedido.objects.filter(status_pedido='PENDENTE').count(),
        'atendidos': Pedido.objects.filter(status_pedido='ATENDIDO').count(),
        'finalizados': Pedido.objects.filter(status_pedido='FINALIZADO').count(),
    }

    contador_new = dados['novos']
    if contador_new > contador_old:
        dados['atualizar_tabela'] = True
        contador_old = contador_new
    else:
        dados['atualizar_tabela'] = False

    return JsonResponse(dados)

# Método utilizado para atualizar a tabela de pedidos novos
@staff_member_required(login_url='/admin/login/')
def renderizar_tabela_pedidos(request):
    pedidos = Pedido.objects.filter(status_pedido='NOVO').order_by('-numero_pedido')
    context = {
        'pedidos': pedidos,
    }
    return render(request, 'table_pedidos.html', context)

