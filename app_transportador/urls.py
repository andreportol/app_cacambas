from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    login_transportador, 
    editar_dados_transportador, 
    IndexTemplateView,
    dados_pedidos,
    tabela_pedidos,
    tabela_pedidos_filtrado,
    detalhes_pedido,
    alterar_status_pedido,
    atualizar_observacao,
    cancelar_pedido,
    Regulamentos,
    PagamentosPedidos,
    ConfirmarPagamento,
    filtro_pagamentos,
)


app_name = 'transportador'

urlpatterns = [
    path('login_transportador/', login_transportador, name='login_transportador'),
    path('index_transportador/', IndexTemplateView.as_view(), name='index_transportador'),
    path('cadastro/', editar_dados_transportador, name='cadastro'),
    path('dados_pedidos/', dados_pedidos, name='dados_pedidos'),
    path('tabela_pedidos/', tabela_pedidos, name='tabela_pedidos'),
    path('tabela_pedidos_filtrado/', tabela_pedidos_filtrado, name='tabela_pedidos_filtrado'),
    path('pedido/<str:numero_pedido>/', detalhes_pedido, name='detalhes_pedido'),
    path('pedido/<str:numero_pedido>/alterar_status/', alterar_status_pedido, name='alterar_status_pedido'),
    path('pedido/<str:numero_pedido>/atualizar_observacao/', atualizar_observacao, name='atualizar_observacao'),
    path('pedido/<str:numero_pedido>/cancelar/', cancelar_pedido, name='cancelar_pedido'),
    path('regulamentos/', Regulamentos.as_view(), name='regulamentos'),
    path('pagamentos/', PagamentosPedidos.as_view(), name='pagamentos_pedidos'),
    path('pagamentos/confirmar/<int:pagamento_id>/', ConfirmarPagamento.as_view(), name='confirmar_pagamento'),
    path('filtro_pagamentos/', filtro_pagamentos, name='filtro_pagamentos'),
]