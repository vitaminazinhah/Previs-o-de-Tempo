import requests
import geocoder
from tkinter import *

from funcoes import LocalizacaoAutomatica, WeatherDataCollector, WeeklyForecastDataFetcher, WeeklyForecast

def obter_localizacao_automatica():
    localizacao = geocoder.ip('me')

    if localizacao.ok:
        lat, lon = localizacao.latlng
        cidade = localizacao.city
        estado = localizacao.state
        pais = localizacao.country

        print(f'{lat},{lon}')
        #print(f'Cidade: {cidade}, Estado: {estado}, País: {pais}')
    else:
        print('Não foi possível obter a localização automaticamente.')
'''
def exibir_previsao_semanal():
    weekly_forecast_instance.update_forecast()
    previsao_text = ""

    if weekly_forecast_instance.weekly_forecast:
        previsao_text += "Previsão Semanal:\n"
        for day in weekly_forecast_instance.weekly_forecast:
            previsao_text += f"{day['date']}: Temperatura: {day['temperature']}°C, Condições: {day['conditions']}\n"
    else:
        previsao_text = "Falha ao obter a previsão semanal."

    previsao_label.config(text=previsao_text)
'''

if __name__ == "__main__":
    obter_localizacao_automatica()

    localizacao_obj = LocalizacaoAutomatica()
    resultado = localizacao_obj.obter_localizacao()
    city_usuario = localizacao_obj.cidade
    country_usuario = localizacao_obj.pais

    print(resultado)

    api_key = '95a2aebd33fc348608c9f6d3ace9c548'

    # INFORMACOES CLIMATICAS COM BASE NA LOCALIZAÇÃO E DATA ATUAL DO USUARIO
    weather_collector = WeatherDataCollector(api_key)
    city_data = weather_collector.collect_weather_data(resultado)

    if city_data:
        print(f"Temperatura da localização atual: {city_data['temperature']}°C")
        print(f"Condições meteorológicas: {city_data['conditions']}")
    else:
        print("Falha ao coletar dados.")


    # INFORMACOES CLIMATICAS DOS PROXIMOS 5 DIAS 
    weekly_data_fetcher = WeeklyForecastDataFetcher(api_key)
    weekly_forecast_instance = WeeklyForecast(weekly_data_fetcher, city_usuario, country_usuario)
    weekly_forecast_instance.update_forecast()
    weekly_forecast_instance.display_forecast()

    


'''
    janela = Tk()
    janela.title("Olha a chuvaaaaaaa")

    # Adicione um botão para exibir a previsão
    botao_previsao = Button(janela, text="Exibir Previsão Semanal", command=exibir_previsao_semanal)
    botao_previsao.pack()

    # Adicione um rótulo para exibir a previsão
    previsao_label = Label(janela, text="")
    previsao_label.pack()

    janela.mainloop()
'''