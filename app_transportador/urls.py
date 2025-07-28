from django.urls import path
from .views import login_transportador, editar_dados_transportador, IndexTemplateView
            

from django.urls import path
from . import views

app_name = 'transportador' # se no módulo urls.py do projeto tem o namespace, esse atributo é obrigatorio 

urlpatterns = [
    path('login_transportador/', login_transportador, name='login_transportador'),
    path('index_transportador/', IndexTemplateView.as_view(), name='index_transportador'),
    path('cadastro/', views.editar_dados_transportador, name='cadastro'),
]