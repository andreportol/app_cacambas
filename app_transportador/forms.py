from django import forms
from core.models import Transportador


class TransportadorLoginForm(forms.Form):
    cnpj = forms.CharField(label='CNPJ', max_length=18)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

class TransportadorForm(forms.ModelForm):
    class Meta:
        model = Transportador
        exclude = ['senha', 'is_ativo']  # você pode também usar `fields = [...]` para escolher campos específicos