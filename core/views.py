from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import ResultadoOrcamentoForm
from geopy.geocoders import Nominatim
from pprint import pprint
import math

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
        # forms.py -> formulario de validação dos dados
        form = ResultadoOrcamentoForm(request.POST)
        if form.is_valid():
            # Recupera os dados validados do formulário
            tamanho = form.cleaned_data.get('tamanho')
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
                'tamanho': tamanho,
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

def geolocalizacao(logradouro, numero, cidade, pais):
    # Instantiate a new Nominatim client
    app = Nominatim(user_agent="my_app")

    # Get location raw data from the user
    your_loc = f'{numero} {logradouro},{cidade}-MS,{pais}'
    location = app.geocode(your_loc)
    latitude = location.latitude
    longitude = location.longitude
    # Print raw data
    pprint(f'latitude = {latitude} {longitude}')
    
def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    # Converter latitude e longitude de graus para radianos
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Diferenças das coordenadas
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula de Haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Raio da Terra em quilômetros (use 6371 para quilômetros, 3956 para milhas)
    r = 6371

    # Distância em quilômetros
    distance = r * c
    return distance

# Latitude e longitude do ponto inicial (por exemplo, -20.5098492, -54.6612137)
lat1 = -20.5098492
lon1 = -54.6612137

# Latitude e longitude de um segundo ponto (exemplo)
lat2 = -23.550520
lon2 = -46.633308

# Calcular a distância
distancia = calcular_distancia_haversine(lat1, lon1, lat2, lon2)
print(f"A distância é de {distancia:.2f} km")