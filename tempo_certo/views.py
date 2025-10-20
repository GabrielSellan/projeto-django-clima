from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from decouple import config
from .forms import ConsultaTempForm
import requests



def busca_clima_view(request):

    cidade = '<Cidade>'
    temperatura = '<Temperatura>'
    erro = None

    if request.method == 'POST':
        form = ConsultaTempForm(request.POST)
        if form.is_valid():
            cidade = form.cleaned_data['cidade']
            api_key = config('OPENWEATHER_API_KEY')
            url = f'http://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={cidade}'

            try:
                resposta = requests.get(url)
                dados = resposta.json()

                if resposta.status_code == 200:
                    cidade = dados['name']
                    temperatura = int(dados['main']['temp'] - 273.15)
                else: 
                    erro = dados.get('message', 'Cidade não encontrada')
                    cidade = None
                    temperatura = None

            except Exception as e:
                erro = f'Ocorreu um erro: {str(e)}'
    
    else:
        form = ConsultaTempForm


    contexto = {
        'form': form,
        'cidade': cidade,
        'temperatura': f"{temperatura}°C" ,
        'erro': erro,
    }
    
    return render(request, 'clima_view/home.html', contexto)
