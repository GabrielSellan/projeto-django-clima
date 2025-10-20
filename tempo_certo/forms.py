from django import forms


class ConsultaTempForm(forms.Form):
    cidade = forms.CharField(label='Digite o local', max_length=100)