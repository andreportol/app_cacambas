from django.urls import path
from .views import IndexTemplateView, ContatoTemplateView, SobrenosTemplateView, \
            OrcamentoForm, resultado_orcamento, confirmar_pedido, aviso_confirmacao, \
            processar_orcamento_regiao_manual, CadastroUsuarioCreateView \

from django.urls import path


app_name = 'core' # se no módulo urls.py do projeto tem o namespace, esse atributo é obrigatorio 

urlpatterns = [
    path('', IndexTemplateView.as_view(),name='index'),
    path('contato/', ContatoTemplateView.as_view(),name='contato'),
    path('sobrenos/', SobrenosTemplateView.as_view(),name='sobrenos'),
    path('orcamento/', OrcamentoForm.as_view(), name='orcamento'),
    path('resultado_orcamento/', resultado_orcamento, name='resultado_orcamento'),
    path('confirmar_pedido/', confirmar_pedido, name='confirmar_pedido'),
    path('aviso_confirmacao/', aviso_confirmacao, name='aviso_confirmacao'),
    path('processar_orcamento_regiao_manual/', processar_orcamento_regiao_manual, name='processar_orcamento_regiao_manual'),
    path('cadastro_usuario/', CadastroUsuarioCreateView.as_view(), name='cadastro_usuario'),
]
