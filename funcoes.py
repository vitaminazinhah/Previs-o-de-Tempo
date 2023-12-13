import requests
from datetime import datetime, timedelta
import geocoder

class LocalizacaoAutomatica:
    def __init__(self):
        self.lat = None
        self.lon = None
        self.cidade = None
        self.estado = None
        self.pais = None

    def obter_localizacao(self):
        localizacao = geocoder.ip('me')
        if localizacao.ok:
            self.lat, self.lon = localizacao.latlng
            self.cidade = localizacao.city
            self.estado = localizacao.state
            self.pais = localizacao.country
            return self.formatar_localizacao()
        else:
            return 'Não foi possível obter a localização automaticamente.'

    def formatar_localizacao(self):
        return f'{self.cidade},{self.estado},{self.pais}'

    def obter_cidade(self):
        return f"{self.cidade}"

    def obter_estado(self):
        return f"{self.estado}"

    def obter_pais(self):
        return f"{self.estado}"

    def obter_lat(self):
        return f"{self.lat}"

    def obter_lon(self):
        return f"{self.lon}"


class WeatherDataCollector:
    def __init__(self, api_key):
        self.api_key = api_key

    def collect_weather_data(self, city):
        endpoint = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            data = response.json()
            temperature = data["main"]["temp"]
            conditions = data["weather"][0]["description"]
            return {"temperature": temperature, "conditions": conditions}
        except requests.exceptions.RequestException as e:
            print(f"Erro ao coletar dados: {e}")
            return None


class HistoricalWeatherDataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'http://api.openweathermap.org/data/2.5/onecall/timemachine'

    def collect_historical_weather(self, lat, lon, date):
        url = f'{self.base_url}?lat={lat}&lon={lon}&dt={date}&appid={self.api_key}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            temperature = data["current"]["temp"]
            conditions = data["current"]["weather"][0]["description"]
            return {"temperature": temperature, "conditions": conditions}
        except requests.exceptions.RequestException as e:
            print(f"Erro ao coletar dados históricos: {e}")
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
            daily_forecasts = [forecast for forecast in data['list'] if forecast['dt_txt'].split()[1] == '12:00:00']
            weekly_forecast = [
                {
                    "date": datetime.fromisoformat(forecast['dt_txt']),
                    "temperature": round(forecast['main']['temp'] - 273.15),
                    "conditions": forecast['weather'][0]['description']
                }
                for forecast in daily_forecasts
            ]
            return weekly_forecast
        except requests.exceptions.RequestException as e:
            print(f"Erro ao coletar dados: {e}")
            return None


class WeeklyForecast:
    def __init__(self, weekly_forecast_data):
        self.weekly_forecast_data = weekly_forecast_data

    @staticmethod
    def get_weekly_forecast(data_fetcher, city, country):
        weekly_forecast_data = data_fetcher.collect_weekly_forecast(city, country)
        return WeeklyForecast(weekly_forecast_data)


class WeatherInfo:
    def __init__(self, api_key):
        self.api_key = api_key
        self.weather_collector = WeatherDataCollector(self.api_key)
        self.historical_data_fetcher = HistoricalWeatherDataFetcher(self.api_key)
        self.weekly_data_fetcher = WeeklyForecastDataFetcher(self.api_key)

    def get_current_weather(self, city):
        return self.weather_collector.collect_weather_data(city)

    def get_historical_weather(self, lat, lon, date):
        return self.historical_data_fetcher.collect_historical_weather(lat, lon, date)

    def get_weekly_forecast(self, city, country):
        return WeeklyForecast.get_weekly_forecast


class WeeklyForecast:
    @staticmethod
    def get_weekly_forecast(data_fetcher, city, country):
        weekly_forecast_data = data_fetcher.collect_weekly_forecast(city, country)
        return weekly_forecast_data