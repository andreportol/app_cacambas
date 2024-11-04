from django.urls import path
from .views import IndexTemplateView, ContatoTemplateView, SobrenosTemplateView, \
            OrcamentoForm, resultado_orcamento, confirmar_pedido, aviso_confirmacao 

app_name = 'core' # se no módulo urls.py do projeto tem o namespace, esse atributo é obrigatorio 

urlpatterns = [
    path('', IndexTemplateView.as_view(),name='index'),
    path('contato/', ContatoTemplateView.as_view(),name='contato'),
    path('sobrenos/', SobrenosTemplateView.as_view(),name='sobrenos'),
    path('orcamento/', OrcamentoForm.as_view(), name='orcamento'),
    path('resultado_orcamento/', resultado_orcamento, name='resultado_orcamento'),
    path('confirmar_pedido/', confirmar_pedido, name='confirmar_pedido'),
    path('aviso_confirmacao/', aviso_confirmacao, name='aviso_confirmacao'),
]
