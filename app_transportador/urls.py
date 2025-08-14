from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    login_transportador, 
    editar_dados_transportador, 
    IndexTemplateView,
    dados_pedidos,
    tabela_pedidos,
    detalhes_pedido,
    alterar_status_pedido,
)


app_name = 'transportador'

urlpatterns = [
    path('login_transportador/', login_transportador, name='login_transportador'),
    path('index_transportador/', IndexTemplateView.as_view(), name='index_transportador'),
    path('cadastro/', editar_dados_transportador, name='cadastro'),
    path('dados_pedidos/', dados_pedidos, name='dados_pedidos'),
    path('tabela_pedidos/', tabela_pedidos, name='tabela_pedidos'),
    path('pedido/<int:pedido_id>/', detalhes_pedido, name='detalhes_pedido'),
    path('pedido/<int:pedido_id>/alterar_status/', alterar_status_pedido, name='alterar_status_pedido'),
]