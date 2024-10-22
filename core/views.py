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
                
                # Buscando a quantidade de produto selecionado
                quantidade_desejada = form.cleaned_data.get('quantidade')
                quantidade_desejada = int(quantidade_desejada)
                
                # Buscando o tipo de resíduo selecionado
                tipo_entulho = form.cleaned_data.get('tipo_residuo')
                
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
                    'tipo_entulho' : tipo_entulho,
                })
            except Bairros_CG.DoesNotExist:
                # Se o bairro não for encontrado, exibe uma mensagem de erro
                # Adicione uma mensagem de erro
                messages.error(request, 'Ocorreu um erro!')
                # buscando informações de form.py
                logradouro = form.cleaned_data.get('logradouro')               
                numero = form.cleaned_data.get('numero') 
                bairro = form.cleaned_data.get('bairro') 
                print(logradouro)
                print(numero)
                print(bairro)
                return render(request, 'regiao_nao_encontrado.html', {                  
                    'error': 'Bairro não cadastrado!',
                    'logradouro': logradouro,
                    'numero' : numero,
                    'bairro': bairro,
                })
    
    # Se não for POST, renderiza o formulário
    form = ResultadoOrcamentoForm()
    return render(request, 'resultado_orcamento.html', 
                {'form': form,
                 })