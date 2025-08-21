from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from .forms import TransportadorLoginForm, TransportadorForm
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView
from core.models import Transportador, TransportadorProduto, Pedido, Pagamento
from django import forms
from django.db.models import Sum
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

# Create your views here.
def login_transportador(request):
    if request.method == 'POST':
        form = TransportadorLoginForm(request.POST)
        if form.is_valid():
            cnpj = form.cleaned_data['cnpj']
            senha = form.cleaned_data['password']

            try:
                transportador = Transportador.objects.get(cnpj=cnpj)
            except Transportador.DoesNotExist:
                form.add_error('cnpj', 'CNPJ não encontrado.')
                return render(request, 'app_transportador/login_transportador.html', {'form': form})

            # Recupera a contagem da sessão (default = 0)
            tentativas = request.session.get('tentativas_login', 0)
            bloqueio_inicio = request.session.get('bloqueio_inicio')  # pode ser None

            # Define duração do bloqueio (ex: 5 minutos)
            duracao_bloqueio = timedelta(minutes=5)

            # Verifica se está bloqueado
            if tentativas >= 3:
                if bloqueio_inicio:
                    # Converte a string ISO para datetime
                    bloqueio_inicio_dt = timezone.datetime.fromisoformat(bloqueio_inicio)

                    agora = timezone.now()
                    tempo_passado = agora - bloqueio_inicio_dt

                    if tempo_passado < duracao_bloqueio:
                        tempo_restante = duracao_bloqueio - tempo_passado
                        minutos = tempo_restante.seconds // 60
                        segundos = tempo_restante.seconds % 60

                        form.add_error(
                            None,
                            f'Número máximo de tentativas excedido. Tente novamente em {minutos} minutos e {segundos} segundos.'
                        )
                        return render(request, 'app_transportador/login_transportador.html', {'form': form})
                    else:
                        # Passou o tempo de bloqueio, reseta contagem e bloqueio
                        request.session['tentativas_login'] = 0
                        del request.session['bloqueio_inicio']
                        tentativas = 0
                        bloqueio_inicio = None
                else:
                    # Se não tem bloqueio_inicio, define agora
                    bloqueio_inicio = timezone.now().isoformat()
                    request.session['bloqueio_inicio'] = bloqueio_inicio

                    form.add_error(
                        None,
                        'Número máximo de tentativas excedido. Tente novamente em 5 minutos.'
                    )
                    return render(request, 'app_transportador/login_transportador.html', {'form': form})

            # Aqui, não está bloqueado, tenta autenticar
            if senha == transportador.senha:
                # Login correto, reseta contagem e bloqueio
                request.session['transportador_id'] = transportador.id
                request.session['tentativas_login'] = 0
                if 'bloqueio_inicio' in request.session:
                    del request.session['bloqueio_inicio']
                return redirect('transportador:index_transportador')
            else:
                # Senha incorreta: incrementa tentativas
                request.session['tentativas_login'] = tentativas + 1
                form.add_error(None, 'Senha incorreta.')

    else:
        form = TransportadorLoginForm()

    return render(request, 'app_transportador/login_transportador.html', {'form': form})


class IndexTemplateView(TemplateView):
    template_name = 'app_transportador/index_transportador.html'

@require_http_methods(["GET", "POST"])
def editar_dados_transportador(request):
    transportador_id = request.session.get('transportador_id')
    if not transportador_id:
        return redirect('app_transportador/index_transportador')

    transportador = get_object_or_404(Transportador, id=transportador_id)

    if request.method == 'POST':
        form = TransportadorForm(request.POST, instance=transportador)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados atualizados com sucesso!')
    else:
        form = TransportadorForm(instance=transportador)

    return render(request, 'app_transportador/editar_dados_transportador.html', {
        'form': form,
        'transportador': transportador,
    })

# Definindo os pedidos para seus respectivos transportadores

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import Http404

@require_http_methods(["GET"])
def dados_pedidos(request):
    transportador_id = request.session.get('transportador_id')
    if not transportador_id:
        return JsonResponse({'error': 'Não autenticado'}, status=401)
    
    try:
        transportador = Transportador.objects.get(id=transportador_id)
        pedidos = Pedido.objects.filter(transportador=transportador)
        
        contadores = {
            'novos': pedidos.filter(status_pedido='NOVO').count(),
            'pendentes': pedidos.filter(status_pedido='PENDENTE').count(),
            'atendidos': pedidos.filter(status_pedido='ATENDIDO').count(),
            'finalizados': pedidos.filter(status_pedido='FINALIZADO').count(),
            'atualizar_tabela': pedidos.filter(status_pedido='NOVO').exists()
        }
        
        return JsonResponse(contadores)
        
    except Transportador.DoesNotExist:
        return JsonResponse({'error': 'Transportador não encontrado'}, status=404)

@require_http_methods(["GET"])
def tabela_pedidos(request):
    transportador_id = request.session.get('transportador_id')
    if not transportador_id:
        return render(request, 'app_transportador/tabela_pedidos.html', {'pedidos': []})
    
    try:
        transportador = Transportador.objects.get(id=transportador_id)
        
        # Obter o parâmetro de status da URL (default: None)
        status = request.GET.get('status')
        
        # Filtrar pedidos por transportador
        pedidos = Pedido.objects.filter(transportador=transportador)
        
        # Aplicar filtro adicional se status for especificado
        if status:
            pedidos = pedidos.filter(status_pedido=status)

        # Ordenar por data de criação (mais recentes primeiro)
        pedidos = pedidos.order_by('-criado')
        
        return render(request, 'app_transportador/tabela_pedidos.html', {
            'pedidos': pedidos,
            'status_filtro': status # opcional: passar para o template
        })

    except Transportador.DoesNotExist:
        return render(request, 'app_transportador/tabela_pedidos.html', {
            'pedidos': []
        })

@require_http_methods(["GET"])
def tabela_pedidos_filtrado(request):
    transportador_id = request.session.get('transportador_id')
    if not transportador_id:
        return render(request, 'app_transportador/tabela_pedidos_filtrado.html', {'pedidos': []})
    
    try:
        transportador = Transportador.objects.get(id=transportador_id)
        
        # Obter o parâmetro de status da URL (default: None)
        status = request.GET.get('status')
        
        # Filtrar pedidos por transportador
        pedidos = Pedido.objects.filter(transportador=transportador)
        
        # Aplicar filtro adicional se status for especificado
        if status:
            pedidos = pedidos.filter(status_pedido=status)

        # Ordenar por data de criação (mais recentes primeiro)
        pedidos = pedidos.order_by('-criado')
        
        return render(request, 'app_transportador/tabela_pedidos_filtrado.html', {
            'pedidos': pedidos,
            'status_filtro': status # opcional: passar para o template
        })

    except Transportador.DoesNotExist:
        return render(request, 'app_transportador/tabela_pedidos_filtrado.html', {
            'pedidos': []
        })

def detalhes_pedido(request, numero_pedido):
    transportador_id = request.session.get('transportador_id')
    if not transportador_id:
        return redirect('transportador:login_transportador')
    
    try:
        transportador = Transportador.objects.get(id=transportador_id)
        pedido = Pedido.objects.get(numero_pedido=numero_pedido, transportador=transportador)
        return render(request, 'app_transportador/detalhes_pedido.html', {'pedido': pedido})
    except Transportador.DoesNotExist:
        raise Http404("Transportador não encontrado")
    
def alterar_status_pedido(request, numero_pedido):
    if not request.session.get('transportador_id'):
        return redirect('transportador:login_transportador')
    
    transportador = get_object_or_404(Transportador, id=request.session['transportador_id'])
    pedido = get_object_or_404(Pedido, numero_pedido=numero_pedido, transportador=transportador)
    
    # Lógica de transição de status
    if pedido.status_pedido == 'NOVO':
        pedido.status_pedido = 'PENDENTE'
        messages.success(request, 'Pedido aceito com sucesso!')
    elif pedido.status_pedido == 'PENDENTE':
        pedido.status_pedido = 'ATENDIDO'
        messages.success(request, 'Caçamba entregue ao cliente e pagamento efetuado!')
    elif pedido.status_pedido == 'ATENDIDO':
        pedido.status_pedido = 'FINALIZADO'
        messages.success(request, 'Caçamba retirada e serviço finalizado!')
    else:
        messages.warning(request, 'Não é possível alterar o status atual.')
        return redirect('transportador:detalhes_pedido', pedido.numero_pedido)
    
    pedido.save()
    return redirect('transportador:detalhes_pedido', pedido.numero_pedido)

from django.http import JsonResponse

def atualizar_observacao(request, numero_pedido):
    if request.method == 'POST':
        try:
            pedido = get_object_or_404(Pedido, numero_pedido=numero_pedido)
            nova_observacao = request.POST.get('observacao', '')
            pedido.observacao = nova_observacao
            pedido.save()
            messages.success(request, 'Observações atualizadas com sucesso!')
        except Exception as e:
            messages.error(request, 'Erro ao salvar observações')
    
    return redirect('transportador:detalhes_pedido', numero_pedido=numero_pedido)

def cancelar_pedido(request, numero_pedido):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, numero_pedido=numero_pedido)
        motivo = request.POST.get('motivo_cancelamento', '').strip()
        
        if not motivo:
            messages.error(request, 'Por favor, informe o motivo do cancelamento.')
            return redirect('transportador:detalhes_pedido', numero_pedido=numero_pedido)
        
        # Atualiza o status e salva o motivo no campo observacao
        pedido.status_pedido = 'CANCELADO'
        
        # Formata o motivo para incluir data/hora e identificação
        from django.utils.timezone import now
        motivo_formatado = f"\n\n--- CANCELAMENTO ({now().strftime('%d/%m/%Y %H:%M')}) ---\nMotivo: {motivo}\n"
        
        # Adiciona ao campo observacao mantendo o conteúdo anterior se existir
        if pedido.observacao:
            pedido.observacao += motivo_formatado
        else:
            pedido.observacao = motivo_formatado
            
        pedido.save()
        
        messages.success(request, 'Pedido cancelado com sucesso.')
        return redirect('transportador:detalhes_pedido', pedido.numero_pedido)
    
    return redirect('transportador:index_transportador')

class Regulamentos(TemplateView):
    template_name = 'app_transportador/regulamentos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'titulo': 'Regulamentos da Plataforma',
            'regras': [
                {
                    'categoria': 'Cadastro e Perfil',
                    'itens': [
                        'Todos os dados cadastrais devem ser verídicos e atualizados',
                        'É obrigatório manter foto atualizada no perfil',
                        'Documentação deve estar sempre válida'
                    ]
                },
                {
                    'categoria': 'Operação e Serviços',
                    'itens': [
                        'Horário de atendimento: 06h às 22h',
                        'Tolerância máxima de atraso: 15 minutos',
                        'Proibido aceitar pagamento em dinheiro diretamente do cliente'
                    ]
                },
                {
                    'categoria': 'Pagamentos',
                    'itens': [
                        'Taxa de serviço: 5% do valor total do pedido',
                        'Pagamentos processados em até 3 dias após a entrega da caçamba',
                    ]
                },
                {
                    'categoria': 'Conduta',
                    'itens': [
                        'Proibido qualquer tipo de discriminação',
                        'Respeitar todas as normas de trânsito'
                    ]
                }
            ]
        })
        return context

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum
from django import forms

from core.models import Pedido, Transportador, Pagamento


# --------------------------
# Pagamentos e Pedidos
# --------------------------
class PagamentosPedidos(TemplateView):
    template_name = 'app_transportador/pagamentos_transportador.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transportador_id = self.request.session.get('transportador_id')

        if not transportador_id:
            context['pedidos'] = []
            context.update(self._estatisticas_vazias())
            return context

        transportador = get_object_or_404(Transportador, id=transportador_id)

        # Todos os pedidos 'ATENDIDOS e FINALIZADOS' do transportador(transportador já recebeu ao deixar a caçamba)
        pedidos = Pedido.objects.filter(
            transportador=transportador,
            status_pedido__in = ['ATENDIDO','FINALIZADO']
            ).order_by('-criado')
        
        # Garante que cada pedido tenha um pagamento PENDENTE
        for pedido in pedidos:
            if not hasattr(pedido, 'pagamento'):
                Pagamento.objects.create(
                    pedido=pedido,
                    valor=pedido.preco,
                    status='PENDENTE',
                    metodo='',
                )

        context['pedidos'] = pedidos
        context.update(self._calcular_estatisticas(pedidos))
        return context

    def _calcular_estatisticas(self, pedidos):
        """
        Calcula totais e separa pendentes e concluídos.
        Considera o objeto Pagamento associado a cada pedido.
        """
        pagamentos = [getattr(pedido, 'pagamento', None) for pedido in pedidos if hasattr(pedido, 'pagamento')]
        pagamentos_pendentes = [p for p in pagamentos if p and p.status == 'PENDENTE']
        pagamentos_aguardados = [p for p in pagamentos if p and p.status == 'AGUARDANDO']
        pagamentos_concluidos = [p for p in pagamentos if p and p.status == 'CONCLUIDO']
       
        from decimal import Decimal
        # todos os pagamentos recebidos pelo transportador na variavel 'pagamentos'
        total_recebido = sum(p.valor for p in pagamentos)
        #todos os pagamentos pendentes
        porcentagem = Decimal(0.05) # 5% do valor recebido 
        total_a_repassar = (sum(p.valor for p in pagamentos_pendentes)) * porcentagem
        
        return {
            'pagamentos_pendentes': pagamentos_pendentes,
            'pagamentos_aguardados': pagamentos_aguardados,
            'pagamentos_concluidos': pagamentos_concluidos,
            'total_recebido': total_recebido,
            'total_a_repassar': total_a_repassar,
        }

    def _estatisticas_vazias(self):
        return {
            'pagamentos_pendentes': [],
            'pagamentos_concluidos': [],
            'total_recebido': 0,
            'total_a_receber': 0,
        }


# --------------------------
# Formulário vazio apenas para o ConfirmarPagamento
# --------------------------
class ConfirmarPagamentoForm(forms.Form):
    """Formulário vazio usado apenas para disparar a ação de confirmação."""
    pass


# --------------------------
# Confirmação de pagamento Vem do template pagamentos_transportador.html, através de um modal 
# --------------------------
class ConfirmarPagamento(FormView):
    form_class = ConfirmarPagamentoForm
    template_name = "app_transportador/confirmar_pagamento.html"  # caso queira exibir algo

    def get_success_url(self):
        return reverse_lazy('transportador:pagamentos_pedidos')

    def form_valid(self, form):
        transportador_id = self.request.session.get('transportador_id')
        if not transportador_id:
            messages.error(self.request, 'Você precisa estar logado como transportador.')
            return redirect('transportador:login_transportador')

        transportador = get_object_or_404(Transportador, id=transportador_id)
        pagamento_id = self.kwargs.get('pagamento_id')

        pagamento = get_object_or_404(
            Pagamento,
            id=pagamento_id,
            pedido__transportador=transportador
        )

        if pagamento.status == 'PENDENTE':
            pagamento.status = 'AGUARDANDO'
            pagamento.save()
            messages.success(
                self.request,
                f'Pagamento do Pedido #{pagamento.pedido.numero_pedido} aguardando confirmação!'
            )
        else:
            messages.warning(self.request, 'Este pagamento já foi confirmado anteriormente.')

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        """
        Para chamadas GET, redireciona para post() simulando a confirmação
        sem precisar exibir um formulário real.
        """
        return self.post(request, *args, **kwargs)
