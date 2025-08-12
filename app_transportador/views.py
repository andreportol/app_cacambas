from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from .forms import TransportadorLoginForm, TransportadorForm
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView
from core.models import Transportador, TransportadorProduto, Pedido

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
        return render(request, 'app_transportador/table_pedidos.html', {'pedidos': []})
    
    try:
        transportador = Transportador.objects.get(id=transportador_id)
        pedidos = Pedido.objects.filter(
            transportador=transportador
        ).order_by('-criado')
        
        return render(request, 'app_transportador/table_pedidos.html', {
            'pedidos': pedidos
        })
    except Transportador.DoesNotExist:
        return render(request, 'app_transportador/table_pedidos.html', {
            'pedidos': []
        })

def detalhes_pedido(request, pedido_id):
    transportador_id = request.session.get('transportador_id')
    if not transportador_id:
        return redirect('transportador:login_transportador')
    
    try:
        transportador = Transportador.objects.get(id=transportador_id)
        pedido = Pedido.objects.get(id=pedido_id, transportador=transportador)
        return render(request, 'app_transportador/detalhes_pedido.html', {'pedido': pedido})
    except Transportador.DoesNotExist:
        raise Http404("Transportador não encontrado")
    except Pedido.DoesNotExist:
        raise Http404("Pedido não encontrado")

def alterar_status_pedido(request, pedido_id):
    if not request.session.get('transportador_id'):
        return redirect('transportador:login_transportador')
    
    transportador = get_object_or_404(Transportador, id=request.session['transportador_id'])
    pedido = get_object_or_404(Pedido, id=pedido_id, transportador=transportador)
    
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
        return redirect('transportador:detalhes_pedido', pedido_id=pedido.id)
    
    pedido.save()
    return redirect('transportador:detalhes_pedido', pedido_id=pedido.id)