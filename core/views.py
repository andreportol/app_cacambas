from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .forms import ResultadoOrcamentoForm, ConfirmarPedidoForm, AvisoConfirmacaoForm, CadastroUsuarioForm
from .models import TransportadorProduto, Produto, Bairros_CG, Transportador, Regiao_CG
from datetime import datetime

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
                request.session['orcamento'] = {
                    'produto': form.cleaned_data.get('produto'),
                    'tipo_entulho': form.cleaned_data.get('tipo_residuo'),
                    'quantidade_desejada': form.cleaned_data.get('quantidade'),
                    'bairro': form.cleaned_data.get('bairro'),
                    'logradouro': form.cleaned_data.get('logradouro'),
                    'num_porta': form.cleaned_data.get('numero'),
                    'cidade': cidade,
                    'data_inicio': str(form.cleaned_data.get('data_inicio')),  # Adicionado
                    'data_retirada': str(form.cleaned_data.get('data_retirada')),  # Adicionado
                }
                return processar_orcamento_campo_grande(request, form)
            else:
                return cidade_nao_atendida(request)
    form = ResultadoOrcamentoForm()
    return render(request, 'resultado_orcamento.html', {'form': form})


def processar_orcamento_campo_grande(request, form=None):  
    # Recuperando dados da sessão e fornecendo valores padrão caso estejam ausentes
    orcamento_data = request.session.get('orcamento', {})
    produto_desejado = orcamento_data.get('produto')
    tipo_entulho = form.cleaned_data.get('tipo_residuo')
    quantidade_desejada = orcamento_data.get('quantidade_desejada')
    data_inicio = form.cleaned_data.get('data_inicio')
    data_retirada = form.cleaned_data.get('data_retirada')
    orcamento_data.update({
        'data_inicio': str(data_inicio),
        'data_retirada': str(data_retirada),
    })
    logradouro = orcamento_data.get('logradouro')
    num_porta = orcamento_data.get('num_porta', 'Número não informado')
    cidade = orcamento_data.get('cidade', 'Cidade não informada')
    bairro_usuario = orcamento_data.get('bairro', '')
    produto_desejado = orcamento_data.get('produto')
    
    try:
        bairro = Bairros_CG.objects.filter(nome_bairro__icontains=bairro_usuario).first()
        regiao_selecionada = buscar_regiao_por_bairro(bairro.nome_bairro)
    except Bairros_CG.DoesNotExist:        
        return render(request, 'regiao_nao_encontrado.html', {
            'bairro': bairro_usuario,
            'logradouro': logradouro,
            'numero': num_porta,
        })

    # Continue o processamento com a região selecionada
    transportadores = buscar_transportadores_por_regiao(regiao_selecionada)  
    produto = verificar_produto(produto_desejado)
     
    if not produto:
        return produto_nao_encontrado(request) 
    
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
        'data_inicio': data_inicio,
        'data_retirada': data_retirada,
        'bairro': bairro_usuario,
        'logradouro': logradouro,
        'num_porta': num_porta,
        'cidade': cidade,
    })


def processar_orcamento_regiao_manual(request):
    if request.method == 'POST':
        # Obtém os dados do orçamento da sessão
        orcamento_data = request.session.get('orcamento', {})
        tipo_entulho = orcamento_data.get('tipo_entulho')
        data_inicio = orcamento_data.get('data_inicio')
        data_retirada = orcamento_data.get('data_retirada')
        logradouro = orcamento_data.get('logradouro')
        num_porta = orcamento_data.get('num_porta', 'Número não informado')
        cidade = orcamento_data.get('cidade', 'Cidade não informada')
        bairro_usuario = orcamento_data.get('bairro', '')
        
        # Recupera a quantidade do produto selecionado
        quantidade_desejada = orcamento_data.get('quantidade_desejada')
        
        # Obtém a região selecionada enviada pelo formulário
        regiao_selecionada = request.POST.get('regiao_urbana', '').upper()
        
        if regiao_selecionada:
            # Atualiza os dados do orçamento com a região selecionada
            orcamento_data.update({'regiao': regiao_selecionada})
            request.session['orcamento'] = orcamento_data

            # Processa os dados com base na região e no orçamento
            transportadores = buscar_transportadores_por_regiao(regiao_selecionada)
          
            produto_desejado = orcamento_data.get('produto')   
            produto = verificar_produto(produto_desejado)
            
            if not produto:
                return produto_nao_encontrado(request)

            transportadores_com_produto = verificar_transportadores_com_produto(
                transportadores, produto_desejado, produto, quantidade_desejada
            )
                
            # Renderiza o template de resultado do orçamento
            return render(request, 'resultado_orcamento.html', {
                'transportadores_com_produto': transportadores_com_produto,
                'regiao_selecionada': regiao_selecionada,
                'produto_desejado': produto,
                'quantidade_desejada': quantidade_desejada,
                'tipo_entulho': tipo_entulho,
                'data_inicio': data_inicio,
                'data_retirada': data_retirada,
                'bairro': bairro_usuario,
                'logradouro': logradouro,
                'num_porta': num_porta,
                'cidade': cidade,
            })

        # Se a região não foi enviada
        return render(request, 'regiao_nao_encontrado.html', {
            'erro': 'Por favor, selecione uma região válida.'
        })


def buscar_regiao_por_bairro(bairro_usuario):
    """
    Busca a região da cidade de acordo com o bairro informado.
    """
    bairro = Bairros_CG.objects.get(nome_bairro__icontains=bairro_usuario)
    return bairro.nome_regiao_regioes


def buscar_transportadores_por_regiao(nome_regiao):
    try:
        regiao = Regiao_CG.objects.get(nome_regiao=nome_regiao)
        return Transportador.objects.filter(regioes_trabalho=regiao)
    except Regiao_CG.DoesNotExist:
        return []


def verificar_produto(produto_desejado):
    """
    Retorna o produto desejado e o objeto do banco de dados correspondente.
    """
    try:
        produto = Produto.objects.get(nome=produto_desejado)
        return produto
    except Produto.DoesNotExist:
        # Retorna None para indicar que o produto não foi encontrado
        return produto_desejado, None


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
        'error': 'Desculpe, mas o produto selecionado não está disponível para o seu bairro!',
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


# Método confirmar_pedido
def confirmar_pedido(request):

    # Recupera os dados existentes da sessão de orçamento
    orcamento_data = request.session.get('orcamento', {})
    
    if request.method == 'POST':
        form = ConfirmarPedidoForm(request.POST)
        if form.is_valid():
            transportador_selecionado = form.cleaned_data.get('transportador_selecionado')         
            if transportador_selecionado:
                # Divide o transportador e preço
                transportador, preco = transportador_selecionado.split('|')
                # Exemplo de dados de sessão com formatação ajustada
                
                data_inicio = orcamento_data.get('data_inicio')
                data_inicio_formatada = datetime.strptime(data_inicio, '%Y-%m-%d').strftime('%d-%m-%Y')
                orcamento_data['data_inicio'] = data_inicio_formatada
                
                data_retirada = orcamento_data.get('data_retirada')
                data_retirada_formatada = datetime.strptime(data_retirada, '%Y-%m-%d').strftime('%d-%m-%Y')
                orcamento_data['data_retirada'] = data_retirada_formatada
                # Atualiza os dados da sessão de orçamento com os novos dados do formulário
                orcamento_data.update({
                    'transportador': transportador,
                    'preco': preco,
                    'produto': form.cleaned_data.get('produto_desejado'),
                    'tipo_entulho': form.cleaned_data.get('tipo_entulho'),
                    'quantidade_desejada': form.cleaned_data.get('quantidade_desejada'),
                    'logradouro': form.cleaned_data.get('logradouro'),
                    'num_porta': form.cleaned_data.get('num_porta'),
                    'bairro': form.cleaned_data.get('bairro'),
                    'cidade': form.cleaned_data.get('cidade'),
                })

                # Salva os dados consolidados na sessão
                request.session['pedido_data'] = orcamento_data

                # Renderiza o template com os dados da sessão
                return render(request, 'confirmar_pedido.html', {'form': form, 'orcamento_data': orcamento_data})
        
        # Se o formulário não for válido, renderiza novamente com o formulário e erros
        return render(request, 'erro_confirmar_pedido.html')
    
    # Se o método não for POST, inicializa o formulário com os dados existentes do orçamento
    form = ConfirmarPedidoForm(initial=orcamento_data)
    return render(request, 'confirmar_pedido.html', {'form': form, 'orcamento_data': orcamento_data})


# Método aviso_confirmacao
def aviso_confirmacao(request):
    if request.method == 'POST':
        form = AvisoConfirmacaoForm(request.POST)
        if form.is_valid():
            nome_cliente = form.cleaned_data.get('nome_cliente')
            telefone_cliente = form.cleaned_data.get('telefone_cliente')
        # Recupera ou inicializa pedido_data com os dados existentes na sessão
        pedido_data = request.session.get('pedido_data', {})
        # Adiciona novos valores ao dicionário pedido_data
        pedido_data.update({
            'nome_cliente': nome_cliente,
            'telefone_cliente': telefone_cliente,
        })
        # Atualiza a sessão com o dicionário pedido_data modificado
        request.session['pedido_data'] = pedido_data
    return render(request, 'aviso_confirmacao.html', pedido_data)

    
    '''
    Recuperar um dicionário chamado pedido_data que foi salvo em request.session
    Se pedido_data não estiver presente na sessão, será retornado um dicionário vazio {} para evitar erros de chave inexistente.
    
    pedido_data = request.session.get('pedido_data', {})
    
    Acesso no template:
    No template aviso_confirmacao.html, você pode acessar as variáveis simplesmente 
    pelo nome das chaves de pedido_data. Por exemplo, se pedido_data contiver 
    {'transportador': 'Transportadora ABC', 'produto': 'Caçamba', 'preco': '200.00'}, 
    você acessará esses valores com {{ transportador }}, {{ produto }}, e {{ preco }} 
    diretamente.
    '''

class CadastroUsuarioCreateView(CreateView):
    template_name = 'cadastro_usuario.html'
    model='Usuario'
    form_class= CadastroUsuarioForm
