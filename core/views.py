from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import ResultadoOrcamentoForm
from .models import TransportadorProduto, Produto, Bairros_CG, Transportador
from django.contrib import messages


# Create your views here.
class IndexTemplateView(TemplateView):
    template_name = 'index.html'

class ContatoTemplateView(TemplateView):
    template_name = 'contato.html'

class SobrenosTemplateView(TemplateView):
    template_name = 'sobrenos.html'

class OrcamentoForm(TemplateView):
    template_name = 'orcamento.html'

def resultado_orcamento(request):
    if request.method == 'POST':
        form = ResultadoOrcamentoForm(request.POST)
        if form.is_valid():
            cidade = form.cleaned_data.get('cidade')

            if cidade == 'Campo Grande':
                return processar_orcamento_campo_grande(request, form)
            else:
                return cidade_nao_atendida(request)

    form = ResultadoOrcamentoForm()
    return render(request, 'resultado_orcamento.html', {'form': form})


def processar_orcamento_campo_grande(request, form):
    bairro_usuario = form.cleaned_data.get('bairro')
    try:
        regiao_selecionada = buscar_regiao_por_bairro(bairro_usuario)
        transportadores = buscar_transportadores_por_regiao(regiao_selecionada)

        produto_desejado, produto = verificar_produto(form)
        if not produto:
            return produto_nao_encontrado(request)

        quantidade_desejada = verificar_quantidade(form)
        tipo_entulho = form.cleaned_data.get('tipo_residuo')

        transportadores_com_produto = verificar_transportadores_com_produto(
            transportadores, produto_desejado, produto, quantidade_desejada
        )

        return render(request, 'resultado_orcamento.html', {
            'form': form,
            'transportadores_com_produto': transportadores_com_produto,
            'regiao_selecionada': regiao_selecionada,
            'produto_desejado': produto,
            'quantidade_desejada': quantidade_desejada,
            'tipo_entulho': tipo_entulho,
        })

    except Bairros_CG.DoesNotExist:
        return bairro_nao_encontrado(request, form)


def buscar_regiao_por_bairro(bairro_usuario):
    """
    Busca a região da cidade de acordo com o bairro informado.
    """
    bairro = Bairros_CG.objects.get(nome_bairro__icontains=bairro_usuario)
    return bairro.nome_regiao_regioes


def buscar_transportadores_por_regiao(regiao_selecionada):
    """
    Busca transportadores que trabalham na região selecionada e estão ativos.
    """
    return Transportador.objects.filter(regioes_trabalho=regiao_selecionada, is_ativo=True)


def verificar_produto(form):
    """
    Verifica se o produto desejado existe e foi selecionado corretamente.
    """
    produto_desejado = form.cleaned_data.get('produto')
    produto = Produto.objects.filter(nome=produto_desejado).first()
    
    return produto_desejado, produto


def verificar_quantidade(form):
    """
    Verifica a quantidade de produtos desejada.
    """
    return int(form.cleaned_data.get('quantidade'))


def verificar_transportadores_com_produto(transportadores, produto_desejado, produto, quantidade_desejada):
    """
    Verifica quais transportadores possuem o produto desejado e calcula o preço.
    """
    transportadores_com_produto = []

    for t in transportadores:
        if t.produtos.filter(nome=produto_desejado).exists():
            transportador_produto = TransportadorProduto.objects.filter(
                transportador=t, produto=produto
            ).first()

            if transportador_produto:
                transportadores_com_produto.append({
                    'transportador': t.nome_fantasia,
                    'preco': transportador_produto.preco * quantidade_desejada
                })

    return sorted(transportadores_com_produto, key=lambda x: x['preco'])


def produto_nao_encontrado(request):
    """
    Renderiza uma página informando que o produto não foi encontrado.
    """
    return render(request, 'produto_nao_encontrado.html', {
        'error': 'Desculpe! O produto selecionado não está disponível para o seu bairro!',
    })


def bairro_nao_encontrado(request, form):
    """
    Renderiza uma página informando que o bairro não foi encontrado.
    """
    logradouro = form.cleaned_data.get('logradouro')
    numero = form.cleaned_data.get('numero')
    bairro = form.cleaned_data.get('bairro')
    
    return render(request, 'regiao_nao_encontrado.html', {                  
        'error': 'Desculpe, mas o bairro não está cadastrado em nosso sistema!',
        'logradouro': logradouro,
        'numero': numero,
        'bairro': bairro,
    })


def cidade_nao_atendida(request):
    """
    Renderiza uma página informando que a cidade não é atendida.
    """
    return render(request, 'cidade_nao_encontrada.html', {
        'error': 'Desculpe, mas no momento não estamos atendendo em sua cidade!',
    })
