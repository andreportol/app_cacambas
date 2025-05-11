from django.urls import path
from .views import IndexTemplateView, dados_pedidos, renderizar_tabela_pedidos,TabelaPedidosNovosListView, TabelaPedidosPendentesListView, TabelaPedidosAtendidosListView, TabelaPedidosFinalizadosListView, TabelaPedidosArquivadosListView, TabelaPedidosCanceladosListView


app_name = 'dashboard' # se no módulo urls.py do projeto tem o namespace, esse atributo é obrigatorio 

urlpatterns = [
    path('', IndexTemplateView.as_view(),name='index_dashboard'),
    path('dashboard/dados/', dados_pedidos, name='dados_pedidos'),
    path('tabela-pedidos/', renderizar_tabela_pedidos, name='tabela_pedidos'),  
    path('pedidos_novos/', TabelaPedidosNovosListView.as_view(), name='tabela_pedidos_novos'),
    path('pedidos_pendentes/', TabelaPedidosPendentesListView.as_view(), name='tabela_pedidos_pendentes'),
    path('pedidos_atendidos/', TabelaPedidosAtendidosListView.as_view(), name='tabela_pedidos_atendidos'),
    path('pedidos_finalizados/', TabelaPedidosFinalizadosListView.as_view(), name='tabela_pedidos_finalizados'),
    path('pedidos_cancelados/', TabelaPedidosCanceladosListView.as_view(), name='tabela_pedidos_cancelados'),
    path('pedidos_arquivados/', TabelaPedidosArquivadosListView.as_view(), name='tabela_pedidos_arquivados'),
]