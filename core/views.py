from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import ResultadoOrcamentoForm
from .models import TransportadorProduto, Produto, Bairros_CG, Transportador
from django.shortcuts import render
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

from django.shortcuts import render

def resultado_orcamento(request):
    if request.method == 'POST':
        form = ResultadoOrcamentoForm(request.POST)
        if form.is_valid():
            # Filtra a cidade
            cidade = form.cleaned_data.get('cidade')
            # se a cidade não for Campo Grande, vai para o else
            if cidade == 'Campo Grande':
                # Filtra o bairro do usuário que solicitou a caçamba
                bairro_usuario = form.cleaned_data.get('bairro')
                        
                # Verifica a qual região de Campo Grande pertence o bairro
                try:
                    '''
                        nome_bairro__icontains=bairro_usuario:
                        -  O __icontains faz uma comparação parcial e insensível a maiúsculas/minúsculas.
                        -  Isso significa que se o usuário digitar "centro" ou apenas parte do nome do bairro, como "cen", o Django ainda encontrará o bairro "Centro". Além disso, não faz distinção entre letras maiúsculas e minúsculas.
                        nome_bairro=bairro_usuario:
                        -  Essa comparação exige que o valor exato do campo nome_bairro no banco de dados seja igual
                            ao valor de bairro_usuario.
                        -  Ou seja, se o usuário digitar "Centro", o sistema só encontrará um bairro chamado exatamente "Centro". Se houver diferenças de maiúsculas e minúsculas ou espaços extras, a busca falhará.
                    '''
                    bairro = Bairros_CG.objects.get(nome_bairro__icontains=bairro_usuario)
                    regiao_selecionada = bairro.nome_regiao_regioes
                    
                    # Buscamos os transportadores que trabalham na região e estão ativos
                    transportadores = Transportador.objects.filter(regioes_trabalho=regiao_selecionada, is_ativo=True)
                            
                    # Buscando o produto desejado
                    produto_desejado = form.cleaned_data.get('produto')
                    produto = Produto.objects.filter(nome=produto_desejado).first()

                    # Verifica se o produto existe
                    if not produto:
                        return render(request, 'produto_nao_encontrado.html', {
                            'error': 'Desculpe! O produto selecionado não está disponível no seu bairro.',
                        })
                    
                    # Lista para armazenar transportadores que têm o produto desejado
                    transportadores_com_produto = []
                    
                    # Buscando a quantidade de produto selecionado
                    quantidade_desejada = int(form.cleaned_data.get('quantidade'))
                    
                    # Buscando o tipo de resíduo selecionado
                    tipo_entulho = form.cleaned_data.get('tipo_residuo')
                    
                    # Verifica quais transportadores possuem o produto desejado
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
                    
                    # Ordena os transportadores pelo preço
                    transportadores_com_produto = sorted(transportadores_com_produto, key=lambda x: x['preco'])

                    # Renderiza os transportadores no template
                    return render(request, 'resultado_orcamento.html', {
                        'form': form,
                        'transportadores_com_produto': transportadores_com_produto,
                        'regiao_selecionada': regiao_selecionada,
                        'produto_desejado': produto,
                        'quantidade_desejada': quantidade_desejada,
                        'tipo_entulho': tipo_entulho,
                    })
                
                except Bairros_CG.DoesNotExist:
                    # Se o bairro não for encontrado, exibe uma mensagem de erro
                    messages.error(request, 'Ocorreu um erro!')
                    logradouro = form.cleaned_data.get('logradouro')
                    numero = form.cleaned_data.get('numero')
                    bairro = form.cleaned_data.get('bairro')
                    
                    return render(request, 'regiao_nao_encontrado.html', {                  
                        'error': 'Bairro não cadastrado!',
                        'logradouro': logradouro,
                        'numero': numero,
                        'bairro': bairro,
                    })
            else:
                return render(request, 'cidade_nao_encontrada.html', {
                    'error': 'Desculpe! No momento não estamos atendendo em sua cidade!',
                })

    # Se não for POST, renderiza o formulário
    form = ResultadoOrcamentoForm()
    return render(request, 'resultado_orcamento.html', {'form': form,})
