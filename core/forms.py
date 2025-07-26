from datetime import timedelta
from django import forms
from django.core.exceptions import ValidationError
from .models import Usuario, Transportador

# formulário de validação do template orcamento.html
class ResultadoOrcamentoForm(forms.Form):
    PRODUTO_CHOICES = [
        ('', 'Escolha'),  # Valor inválido para seleção padrão
        ('cacamba_2m', 'Caçamba 2m³'),
        ('cacamba_3m', 'Caçamba 3m³'),
        ('cacamba_4m', 'Caçamba 4m³'),
        ('caminhao_5m', 'Caminhão 5m³'),
        ('caminhao_12m', 'Caminhão 12m³'),
        ('caminhao_25m', 'Caminhão 25m³'),
        ('roll_roll_25', 'Roll Roll 25m³'),
        ('roll_roll_32', 'Roll Roll 32m³'),
    ]

    TIPO_RESIDUO_CHOICES = [
        ('', 'Escolha'),  # Valor inválido para seleção padrão
        ('classe_A', 'CLASSE A - Alvenarias, concreto, argamassas e solos.'),
        ('classe_B', 'CLASSE B - Restos de madeira, metal, plástico, papel, papelão, vidros.'),
        ('classe_A/B', 'CLASSE A/B - Resíduos com materiais classe A e classe B.'),
        ('classe_C', 'CLASSE C - Resíduos sem tecnologia para reciclagem (gesso e isopor).'),
        ('classe_D', 'CLASSE D - Resíduos perigosos, tais como tintas, solventes, óleos e outros, ou aqueles contaminados procedente de obras em clínicas radiológicas, hospitais, instalações industriais, etc..')
    ]
    produto = forms.ChoiceField(choices=PRODUTO_CHOICES, required=True)
    tipo_residuo = forms.ChoiceField(choices=TIPO_RESIDUO_CHOICES, required=True)
    quantidade = forms.IntegerField(max_value=10, min_value=1, required=True)
        
    # função de validação do produto
    def clean_produto(self):
        produto = self.cleaned_data.get('produto')
        if not produto or produto not in ['cacamba_2m','cacamba_3m','cacamba_4m', 'caminhao_5m', 'caminhao_12m','caminhao_25m','roll_roll_25','roll_roll_32']:
            raise forms.ValidationError("Por favor, selecione um produto válido.")
        return produto
    
    # função de validação do tipo de resíduo
    def clean_tipo_residuo(self):
        tipo_residuo = self.cleaned_data.get('tipo_residuo')
        if not tipo_residuo or tipo_residuo not in ['classe_A', 'classe_B', 'classe_A/B', 'classe_C', 'classe_D']:
            raise forms.ValidationError("Por favor, selecione um tipo de resíduo válido.")
        return tipo_residuo  
    
    data_inicio = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    data_retirada = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    
    # função de validação de data
    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_retirada = cleaned_data.get('data_retirada')

        # Verifica se as duas datas estão preenchidas
        if data_inicio and data_retirada:
            # Valida se a data de início é maior que a data de retirada
            if data_inicio > data_retirada:
                raise ValidationError("A data de início não pode ser maior que a data de retirada.")
        
        # Verifica se a diferença entre as duas datas não é superior a 9 dias
        if data_inicio and data_retirada:
            # Valida se a data de início é maior que a data de retirada
            if (data_retirada - data_inicio) > timedelta(days=9):
                raise ValidationError("A quantidade de dias não pode ser superior a 9 dias.")

        return cleaned_data
    
    cep = forms.CharField(max_length=9)
    logradouro = forms.CharField(max_length=100)
    numero = forms.CharField(max_length=10)
    bairro = forms.CharField(max_length=80)
    cidade = forms.CharField(max_length=100)


class ConfirmarPedidoForm(forms.Form):
    transportador_selecionado = forms.CharField(max_length=120)
    produto_desejado = forms.CharField(max_length=50)
    tipo_entulho = forms.CharField(max_length=15)
    quantidade_desejada = forms.CharField(max_length=12)
    logradouro = forms.CharField(max_length=100)
    num_porta = forms.CharField(max_length=10)
    bairro = forms.CharField(max_length=80)
    cidade = forms.CharField(max_length=100)
    #data_inicio = forms.CharField(max_length=12)
    #data_retirada = forms.CharField(max_length=12)
    

class AvisoConfirmacaoForm(forms.Form):
    nome_cliente = forms.CharField(max_length=120)
    telefone_cliente = forms.CharField(max_length=15)

class CadastroUsuarioForm(forms.ModelForm):
    class Meta:
        # Modelo base
        model = Usuario
        fields = [
            'nome_usuario',
            'telefone',
        ]


class TransportadorLoginForm(forms.Form):
    cnpj = forms.CharField(label='CNPJ', max_length=18)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

# forms.py
from django import forms
from .models import Transportador

class TransportadorForm(forms.ModelForm):
    class Meta:
        model = Transportador
        exclude = ['senha']  # você pode também usar `fields = [...]` para escolher campos específicos
