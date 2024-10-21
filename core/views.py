from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import ResultadoOrcamentoForm
from .models import Regiao_CG, Transportador, TransportadorProduto, Produto

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

def resultado_orcamento_1(request):
    if request.method == 'POST':
        # forms.py -> formulario de validação dos dados
        form = ResultadoOrcamentoForm(request.POST)
        if form.is_valid():
            # Recupera os dados validados do formulário
            produto = form.cleaned_data.get('produto')
            tipo_residuo = form.cleaned_data.get('tipo_residuo')
            quantidade = form.cleaned_data.get('quantidade')
            data_inicio = form.cleaned_data.get('data_inicio')
            data_retirada = form.cleaned_data.get('data_retirada')
            cep = form.cleaned_data.get('cep')
            logradouro = form.cleaned_data.get('logradouro')
            numero = form.cleaned_data.get('numero')
            bairro = form.cleaned_data.get('bairro')
            cidade = form.cleaned_data.get('cidade')
            # método para georeferenciar o endereço
            #geolocalizacao(logradouro, numero, cidade='Campo Grande', pais='Brasil')

            # Passa os dados para o template
            context = {
                'produto': produto,
                'tipo_residuo': tipo_residuo,
                'quantidade': quantidade,
                'data_inicio': data_inicio,
                'data_retirada': data_retirada,
                'cep': cep,
                'logradouro': logradouro,
                'numero': numero,
                'bairro': bairro,
                'cidade': cidade
            }
            return render(request, 'resultado_orcamento.html', context)
        else:
            # Se o formulário for inválido, ele exibirá os erros no template de erro_preenchimento_orcamento
            return render(request, 'erro_preenchimento_orcamento.html', {'form': form})
    else:
        form = ResultadoOrcamentoForm()
    return render(request, 'erro_preenchimento_orcamento.html', {'form': form})

from django.shortcuts import render
from .models import Bairros_CG, Regiao_CG, Transportador

def resultado_orcamento(request):
    if request.method == 'POST':
        form = ResultadoOrcamentoForm(request.POST)
        if form.is_valid():
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
                
                # Agora buscamos os transportadores que trabalham na região e estão ativos
                transportadores = Transportador.objects.filter(regioes_trabalho=regiao_selecionada, is_ativo=True)
                          
                # Buscando o preço do produto por transportador
                produto_desejado = form.cleaned_data.get('produto')
                produto = Produto.objects.get(nome=produto_desejado)  # Aqui você busca o objeto do produto pelo nome
                
                # Lista para armazenar transportadores que têm o produto desejado
                transportadores_com_produto = []
                
                # Quantidade de produto selecionado
                quantidade_desejada = form.cleaned_data.get('quantidade')
                quantidade_desejada = int(quantidade_desejada)
                
                for t in transportadores:
                    # Verifica se o transportador possui o produto desejado
                    if t.produtos.filter(nome=produto_desejado).exists():
                        # Encontra o preço do produto para o transportador
                        transportador_produto = TransportadorProduto.objects.get(transportador=t, produto__nome=produto_desejado)
                        
                        # Adiciona o transportador e o preço à lista
                        transportadores_com_produto.append({
                            'transportador': t.nome_fantasia,  # Nome do transportador
                            'preco': transportador_produto.preco * quantidade_desejada # Preço do produto
                        })

                # Ordena a lista de transportadores pelo preço (em ordem crescente)
                transportadores_com_produto = sorted(transportadores_com_produto, key=lambda x: x['preco'])

                # Renderiza os transportadores no template (aqui você poderia passar os transportadores para o template)
                return render(request, 'resultado_orcamento.html', {
                    'form': form,
                    'transportadores_com_produto': transportadores_com_produto,
                    'regiao_selecionada': regiao_selecionada,
                    'produto_desejado' : produto,
                    'quantidade_desejada' : quantidade_desejada,
                })
            except Bairros_CG.DoesNotExist:
                # Se o bairro não for encontrado, exibe uma mensagem de erro
                print("Bairro não encontrado.")
                return render(request, 'resultado_orcamento.html', {
                    'form': form,
                    'error': 'Bairro não encontrado.',
                })
    
    # Se não for POST, renderiza o formulário
    form = ResultadoOrcamentoForm()
    return render(request, 'resultado_orcamento.html', {'form': form})