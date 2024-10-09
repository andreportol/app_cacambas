from datetime import timedelta
from django import forms
from django.core.exceptions import ValidationError

# formulário de validação do template orcamento.html
class ResultadoOrcamentoForm(forms.Form):
    TAMANHO_CHOICES = [
        ('', 'Escolha'),  # Valor inválido para seleção padrão
        ('2', 'caçamba de 2 m³'),
        ('3', 'caçamba de 3 m³'),
        ('4', 'caçamba de 4 m³'),
        ('5', 'caminhão de 5 m³'),
        ('12', 'caminhão de 12 m³'),
        ('25', 'caminhão de 25 m³'),
        ('25_roll', 'Roll on roll off 25 m³'),
        ('32_roll', 'Roll on roll off 32 m³'),
    ]

    TIPO_RESIDUO_CHOICES = [
        ('', 'Escolha'),  # Valor inválido para seleção padrão
        ('classe_A', 'CLASSE A - Alvenarias, concreto, argamassas e solos.'),
        ('classe_B', 'CLASSE B - Restos de madeira, metal, plástico, papel, papelão, vidros.'),
        ('classe_A/B', 'CLASSE A/B - Resíduos com materiais classe A e classe B.'),
        ('classe_C', 'CLASSE C - Resíduos sem tecnologia para reciclagem (gesso e isopor).'),
        ('classe_D', 'CLASSE D - Resíduos perigosos, tais como tintas, solventes, óleos e outros, ou aqueles contaminados procedente de obras em clínicas radiológicas, hospitais, instalações industriais, etc..')
    ]

    QUANTIDADE_CHOICES = [
        ('', 'Escolha'),  # Valor inválido para seleção padrão
        ('1', '1 - Uma'),
        ('2', '2 - Duas'),
        ('3', '3 - Três'),
    ]


    tamanho = forms.ChoiceField(choices=TAMANHO_CHOICES, required=True)
    tipo_residuo = forms.ChoiceField(choices=TIPO_RESIDUO_CHOICES, required=True)
    quantidade = forms.ChoiceField(choices=QUANTIDADE_CHOICES, required=True)
    
    # função de validação do tamanho
    def clean_tamanho(self):
        tamanho = self.cleaned_data.get('tamanho')
        if not tamanho or tamanho not in ['2','3','4', '5', '12','25','25_roll','32_roll']:
            raise forms.ValidationError("Por favor, selecione um tamanho válido.")
        return tamanho
    
    # função de validação do tipo de resíduo
    def clean_tipo_residuo(self):
        tipo_residuo = self.cleaned_data.get('tipo_residuo')
        if not tipo_residuo or tipo_residuo not in ['classe_A', 'classe_B', 'classe_A/B', 'classe_C', 'classe_D']:
            raise forms.ValidationError("Por favor, selecione um tipo de resíduo válido.")
        return tipo_residuo
    
    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        if not quantidade or quantidade not in ['1', '2', '3']:
            raise forms.ValidationError("Por favor, selecione uma quantidade válida.")
        return quantidade
    
    
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
