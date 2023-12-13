import tkinter as tk
from tkinter import messagebox
import webbrowser
import folium
from datetime import datetime, timedelta
from funcoes import LocalizacaoAutomatica, WeatherDataCollector, WeeklyForecastDataFetcher, WeeklyForecast, HistoricalWeatherDataFetcher


class ResultWindow:
    def __init__(self, parent, city_data, weekly_forecast_data):
        self.result_window = tk.Toplevel(parent)
        self.result_window.title("Resultados da Busca")

        if city_data:
          
            tk.Label(self.result_window, text=f"Temperatura Atual: {city_data['temperature']}°C").pack(pady=12)
            tk.Label(self.result_window, text=f"Condições Atuais: {city_data['conditions']}").pack(pady=12)

            tk.Label(self.result_window, text="Previsão para os Próximos 5 Dias:", font=('Helvetica', 12, 'bold')).pack(pady=10)

            if weekly_forecast_data:
                for day in weekly_forecast_data:
                    forecast_text = f"{day['date'].strftime('%Y-%m-%d')}: {day['temperature']}°C, {day['conditions']}"
                    tk.Label(self.result_window, text=forecast_text, font=('Helvetica', 10)).pack(anchor='w')
            else:
                tk.Label(self.result_window, text="Falha ao obter a previsão para os próximos 5 dias.", font=('Helvetica', 10)).pack(pady=10)
        else:
            tk.Label(self.result_window, text="Erro ao obter dados da cidade.", font=('Helvetica', 10)).pack(pady=10)


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Consulta Meteorológica")

        localizacao_obj = LocalizacaoAutomatica()
        resultado = localizacao_obj.obter_localizacao()
        self.city_usuario = localizacao_obj.obter_cidade()
        self.country_usuario = localizacao_obj.obter_pais()
        self.lat_usuario = localizacao_obj.obter_lat()
        self.lon_usuario = localizacao_obj.obter_lon()

        self.api_key = '95a2aebd33fc348608c9f6d3ace9c548'
        self.weather_collector = WeatherDataCollector(self.api_key)
        self.city_data = self.weather_collector.collect_weather_data(f"{self.city_usuario},{self.country_usuario}")

        # Obtém a previsão para os próximos cinco dias
        self.weekly_data_fetcher = WeeklyForecastDataFetcher(self.api_key)
        self.weekly_forecast_data = WeeklyForecast.get_weekly_forecast(self.weekly_data_fetcher, self.city_usuario, self.country_usuario)

        # Criação da interface gráfica
        self.create_widgets()

    def create_widgets(self):
        # Estilo para deixar a interface mais agradável
        self.root.geometry("400x550")  # Ajustei a altura para acomodar o novo campo
        self.root.configure(bg='#E5E5E5')  # Cor de fundo
        self.root.resizable(False, False)  # Torna a janela não redimensionável

        # Informações climáticas atuais
        self.lbl_city = tk.Label(self.root, text=f"Localização Atual: {self.city_usuario}", font=('Helvetica', 12, 'bold'), bg='#E5E5E5')
        self.lbl_temperature = tk.Label(self.root, text="Temperatura Atual: -", font=('Helvetica', 12, 'bold'), bg='#E5E5E5')
        self.lbl_conditions = tk.Label(self.root, text="Condições Atuais: -", font=('Helvetica', 12, 'bold'), bg='#E5E5E5')

        # Informações climáticas históricas
        # self.lbl_historical_temperature = tk.Label(self.root, text=" ")
        # self.lbl_historical_conditions = tk.Label(self.root, text=" ")

       
        self.lbl_weekly_forecast = tk.Label(self.root, text="Previsão para os Próximos 5 Dias:", font=('Helvetica', 13, 'bold'), bg='#E5E5E5')

        # Container para a previsão semanal
        self.frame_weekly_forecast = tk.Frame(self.root, bg='#E5E5E5')

        # Botão para obter dados históricos
        self.btn_get_historical_data = tk.Button(self.root, text="Obter Dados Históricos", command=self.get_historical_data, font=('Helvetica', 10), bg='#4CAF50', fg='white')

        # Botão para abrir o mapa
        self.btn_open_map = tk.Button(self.root, text="Abrir Mapa", command=self.open_map, font=('Helvetica', 10), bg='#2196F3', fg='white')

        # Campo de busca
        self.entry_city_search = tk.Entry(self.root, font=('Helvetica', 12))
        self.entry_city_search.insert(0, "")  # Texto padrão
        self.lbl_search_message = tk.Label(self.root, text="Buscar nova localização", font=('Helvetica', 12, 'bold'), bg='#E5E5E5')
        self.l_search_message = tk.Label(self.root, text="Padrão: Cidade, Pais", font=('Helvetica', 8), bg='#E5E5E5')
        # Botão de busca
        self.btn_search = tk.Button(self.root, text="Buscar", command=self.search_city, font=('Helvetica', 10, 'bold'), bg='#FFD700')  # Cor amarela

        # Posiciona os widgets
        self.lbl_city.pack(pady=10)
        self.lbl_temperature.pack(pady=10)
        self.lbl_conditions.pack(pady=10)
        self.lbl_weekly_forecast.pack(pady=10)
        self.frame_weekly_forecast.pack(pady=10)
        self.btn_get_historical_data.pack(pady=10)
        self.btn_open_map.pack(pady=10)
        self.lbl_search_message.pack(pady=5)
        self.l_search_message.pack(pady=5)
        self.entry_city_search.pack(pady=5)
        self.btn_search.pack(pady=10)

        # Exibe a previsão inicialmente
        self.display_current_weather()
        self.display_weekly_forecast()

    def get_historical_data(self):
       
        historical_data_fetcher = HistoricalWeatherDataFetcher(self.api_key)
        historical_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        self.historical_data = historical_data_fetcher.collect_historical_weather(self.lat_usuario, self.lon_usuario, historical_date)

        if self.historical_data:
        
            messagebox.showinfo("Dados Históricos", f"Temperatura Histórica: {self.historical_data['temperature']}°C\nCondições Históricas: {self.historical_data['conditions']}")
        else:
            messagebox.showerror("Erro", "Falha ao obter dados históricos.")

    def display_current_weather(self):
        if self.city_data:
            self.lbl_temperature.config(text=f"Temperatura Atual: {self.city_data['temperature']}°C")
            self.lbl_conditions.config(text=f"Condições Atuais: {self.city_data['conditions']}")
        else:
            messagebox.showerror("Erro", "Falha ao obter dados climáticos atuais.")

    def display_weekly_forecast(self):
        if self.weekly_forecast_data:
            for day in self.weekly_forecast_data:
                forecast_text = f"{day['date'].strftime('%Y-%m-%d')}: {day['temperature']}°C, {day['conditions']}"
                tk.Label(self.frame_weekly_forecast, text=forecast_text, font=('Helvetica', 10), bg='#E5E5E5').pack(anchor='w')
        else:
            messagebox.showerror("Erro", "Falha ao obter a previsão para os próximos 5 dias.")

    def open_map(self):
        # Cria um mapa centrado na localização atual
        mapa = folium.Map(location=[float(self.lat_usuario), float(self.lon_usuario)], zoom_start=10)

        # Adiciona um marcador com informações sobre a localização
        popup_text = f"Localização: ({self.lat_usuario}, {self.lon_usuario})\nTemperatura Atual: {self.city_data['temperature']}°C"
        folium.Marker([float(self.lat_usuario), float(self.lon_usuario)], popup=popup_text).add_to(mapa)

        # Salva o mapa em um arquivo HTML temporário
        mapa.save("temp_mapa_meteorologico.html")

        # Abre o mapa em um navegador externo
        webbrowser.open("temp_mapa_meteorologico.html", new=2)

    def search_city(self):
       
        city_and_country = self.entry_city_search.get()
        city_and_country = city_and_country.split(",")  
        if len(city_and_country) == 2:
            self.city_usuario, self.country_usuario = map(str.strip, city_and_country)
            self.city_data = self.weather_collector.collect_weather_data(f"{self.city_usuario},{self.country_usuario}")
            self.weekly_forecast_data = WeeklyForecast.get_weekly_forecast(self.weekly_data_fetcher, self.city_usuario, self.country_usuario)

            
            ResultWindow(self.root, self.city_data, self.weekly_forecast_data)
        else:
            messagebox.showwarning("Aviso", "Por favor, insira a cidade e o país separados por vírgula.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
