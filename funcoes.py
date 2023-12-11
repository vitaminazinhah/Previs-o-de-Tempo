import geocoder
import requests
from datetime import datetime, timedelta


   
#classe teste localização usuario geral
class LocalizacaoAutomatica:
    def __init__(self):
        self.lat = None
        self.lon = None
        self.cidade = None
        self.estado = None
        self.pais = None

    def obter_localizacao(self):
        # Obtém a localização do usuário usando o endereço IP
        localizacao = geocoder.ip('me')

        # Verifica se a localização foi obtida com sucesso
        if localizacao.ok:
            self.lat, self.lon = localizacao.latlng
            self.cidade = localizacao.city
            self.estado = localizacao.state
            self.pais = localizacao.country

            return self.formatar_localizacao()
        else:
            return 'Não foi possível obter a localização automaticamente.'

    def formatar_localizacao(self):
        return (
            f'{self.cidade},{self.estado},{self.pais}'
        )
    def obter_cidade(self):
        return f"{self.cidade}"
    def obter_estado(self):
        return f"{self.estado}"
    def obter_pais(self):
        return f"{self.estado}"

    
    
class WeatherDataCollector:
    def __init__(self, api_key):
        self.api_key = api_key

    def collect_weather_data(self, city):
        # Endpoint da OpenWeatherMap API para previsão atual
        endpoint = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"

        try:
            # Fazendo a requisição à API
            response = requests.get(endpoint)
            response.raise_for_status()  # Lança uma exceção para códigos de erro HTTP

            # Processa os dados da resposta JSON
            data = response.json()
            temperature = data["main"]["temp"]
            conditions = data["weather"][0]["description"]

            return {"temperature": temperature, "conditions": conditions}
        except requests.exceptions.RequestException as e:
            print(f"Erro ao coletar dados: {e}")
            return None


class WeeklyForecastDataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'http://api.openweathermap.org/data/2.5/forecast'

    def collect_weekly_forecast(self, city, country):
        url = f'{self.base_url}?q={city},{country}&appid={self.api_key}'

        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            # Filtra os dados para obter apenas a previsão para os próximos 5 dias
            daily_forecasts = [forecast for forecast in data['list'] if forecast['dt_txt'].split()[1] == '12:00:00']

            weekly_forecast = [
                {
                    "date": datetime.fromisoformat(forecast['dt_txt']),
                    "temperature": round(forecast['main']['temp'] - 273.15),  # Convertendo para Celsius e arredondando
                    "conditions": forecast['weather'][0]['description']
                }
                for forecast in daily_forecasts
            ]

            return weekly_forecast

        except requests.exceptions.RequestException as e:
            print(f"Erro ao coletar dados: {e}")
            return None



class WeeklyForecast:
    def __init__(self, data_fetcher, city, country):
        self.data_fetcher = data_fetcher
        self.city = city
        self.country = country
        self.weekly_forecast = None

    def update_forecast(self):
        # Coleta a previsão para os próximos 5 dias usando o WeeklyForecastDataFetcher
        self.weekly_forecast = self.data_fetcher.collect_weekly_forecast(self.city, self.country)

    def display_forecast(self):
        if self.weekly_forecast:
            print("Previsão para os Próximos 5 Dias:")
            for day in self.weekly_forecast:
                print(f"Data: {day['date']}, Temperatura: {day['temperature']}°C, Condição: {day['conditions']}")
        else:
            print("Falha ao obter a previsão para os próximos 5 dias.")

