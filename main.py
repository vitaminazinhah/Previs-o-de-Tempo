import requests
import geocoder
from tkinter import *

import tkinter as tk
import webbrowser
import folium

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

if __name__ == "__main__":
    obter_localizacao_automatica()

    localizacao_obj = LocalizacaoAutomatica()
    resultado = localizacao_obj.obter_localizacao()
    city_usuario = localizacao_obj.cidade
    country_usuario = localizacao_obj.pais
    lat_usuario= localizacao_obj.lat
    lon_usuario= localizacao_obj.lon

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



url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat_usuario}&lon={lon_usuario}&appid={api_key}"

# Crie um mapa centrado na localização
mapa = folium.Map(location=[lat_usuario, lon_usuario], zoom_start=10)

popup_text = f"Localização: ({lat_usuario}, {lon_usuario})\nTemperatura: {city_data['temperature']}°C"
folium.Marker([lat_usuario, lon_usuario], popup=popup_text).add_to(mapa)

# salvando o mapa em um arquivo HTML temporário
mapa.save("temp_mapa_meteorologico.html")

# abrir o mapa em um navegador externo
def abrir_mapa():
    webbrowser.open("temp_mapa_meteorologico.html", new=2)


root = tk.Tk()
root.title("Mapa Meteorológico")
abrir_mapa_button = tk.Button(root, text="Abrir Mapa", command=abrir_mapa)
abrir_mapa_button.pack(pady=10)
root.mainloop()