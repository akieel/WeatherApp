import tkinter as tk
from tkinter import ttk, messagebox
import requests
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math
from PIL import Image, ImageTk, ImageOps

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.api_key = "0bdb263ccdd84296dc6a57e50fbcd336"
        self.units_var = tk.StringVar(value="metric")
        self.setup_ui()

    def setup_ui(self):
        self.root.configure(background='#333')
        style = ttk.Style(self.root)
        style.configure('TFrame', background='#333')
        style.configure('TLabel', background='#333', foreground='#FFF', font=('Arial', 11))
        style.configure('TEntry', foreground='#333', font=('Arial', 11))
        style.configure('TButton', font=('Arial', 11, 'bold'), borderwidth=1)
        style.map('TButton', background=[('active', '#0052cc'), ('!disabled', '#0066ff')])
        style.configure('TRadiobutton', background='#333', foreground='#FFF', font=('Arial', 11))

        # Main frame
        self.frame = ttk.Frame(self.root)
        self.frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

        # City input area
        self.city_input_frame = ttk.Frame(self.frame, style='TFrame')
        self.city_input_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ttk.Label(self.city_input_frame, text="Enter City:", style='TLabel').grid(row=0, column=0, padx=5, sticky="w")
        self.city_entry = ttk.Entry(self.city_input_frame, font=('Arial', 14))
        self.city_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Unit selection area
        self.unit_selection_frame = ttk.Frame(self.frame, style='TFrame')
        self.unit_selection_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Radiobutton(self.unit_selection_frame, text="Celsius", variable=self.units_var, value="metric", style='TRadiobutton').grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(self.unit_selection_frame, text="Fahrenheit", variable=self.units_var, value="imperial", style='TRadiobutton').grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Weather and forecast buttons area
        self.buttons_frame = ttk.Frame(self.frame, style='TFrame')
        self.buttons_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.get_weather_button = ttk.Button(self.buttons_frame, text="Get Weather", command=self.get_weather, style='TButton')
        self.get_weather_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.get_forecast_button = ttk.Button(self.buttons_frame, text="Get Weather Forecast", command=self.get_weather_forecast, style='TButton')
        self.get_forecast_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Forecast display area
        self.weather_frame = ttk.Frame(self.frame, padding=5, style='TFrame')
        self.weather_frame.grid(row=2, column=0, columnspan=5, pady=10, sticky="nsew")

           
    def fetch_data(self, city, endpoint="weather"):
        url = f"http://api.openweathermap.org/data/2.5/{endpoint}?q={city}&appid={self.api_key}&units={self.units_var.get()}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            error_message = response.json().get('message', 'Unknown error')
            raise requests.HTTPError(f"Error fetching data: {error_message}")

    def display_weather(self, data):
        
        for widget in self.weather_frame.winfo_children():
            widget.destroy()

        temp = data['main']['temp']
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        wind_deg = data['wind']['deg']
        unit_label = "°C" if self.units_var.get() == 'metric' else "°F"
        modern_font = ("Helvetica", 14)

        
        ttk.Label(self.weather_frame, text=f"Temperature:\n{temp}{unit_label}", font=modern_font).grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(self.weather_frame, text=f"Description:\n{description}", font=modern_font).grid(row=1, column=0, padx=10, pady=5)
        ttk.Label(self.weather_frame, text=f"Humidity:\n{humidity}%", font=modern_font).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(self.weather_frame, text=f"Pressure:\n{pressure} hPa", font=modern_font).grid(row=1, column=1, padx=10, pady=5)
        ttk.Label(self.weather_frame, text=f"Wind Speed:\n{wind_speed} meter/sec", font=modern_font).grid(row=0, column=2, padx=10, pady=5)
        ttk.Label(self.weather_frame, text=f"Wind Direction:\n{wind_deg}°", font=modern_font).grid(row=1, column=2, padx=10, pady=5)

        
        
        self.plot_hourly_forecast(data['name'])

    def plot_hourly_forecast(self, city):
        forecast_data = self.fetch_data(city, "forecast")
        fig = Figure(figsize=(6, 4), dpi=100)
        plot = fig.add_subplot(1, 1, 1)

        times = [datetime.datetime.fromtimestamp(forecast['dt']).strftime('%H:%M') for forecast in forecast_data['list'][:8]]
        temps = [forecast['main']['temp'] for forecast in forecast_data['list'][:8]]

        plot.plot(times, temps, marker='o', linestyle='-', color='black')  
        plot.set(title='Hourly Temperature Forecast', xlabel='Time', ylabel=f'Temperature ({self.units_var.get()})')

   
        plot.spines['top'].set_visible(False)
        plot.spines['right'].set_visible(False)
        plot.spines['bottom'].set_color('lightgray')
        plot.spines['left'].set_color('lightgray')
        plot.xaxis.set_tick_params(color='lightgray')
        plot.yaxis.set_tick_params(color='lightgray')
        plot.grid(color='lightgray', linestyle='dotted')

        canvas = FigureCanvasTkAgg(fig, master=self.weather_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=3, column=0, columnspan=5, pady=10)

    def get_weather(self):
        city = self.city_entry.get()
        if city:
            try:
                weather_data = self.fetch_data(city, "weather")
                self.display_weather(weather_data)
            except requests.HTTPError as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showinfo("Error", "Please enter a city")

     

    def get_weather_forecast(self):
        city = self.city_entry.get()
        if city:
            try:
                forecast_data = self.fetch_data(city, "forecast")
                daily_forecasts = self.process_daily_forecast(forecast_data)
                self.display_daily_forecast(daily_forecasts)
            except requests.HTTPError as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showinfo("Error", "Please enter a city")

    def display_daily_forecast(self, forecasts):
    
        for widget in self.weather_frame.winfo_children():
            widget.destroy()

    
        self.daily_forecast_frame = ttk.Frame(self.weather_frame)
        self.daily_forecast_frame.grid(row=0, column=0, sticky="nsew")

        for index, (date, forecast) in enumerate(forecasts.items()):
        
            ttk.Label(self.daily_forecast_frame, text=date).grid(row=index, column=0, padx=5, pady=5, sticky="w")

        
            temp_label = f"{forecast['max_temp']}°/{forecast['min_temp']}°"
            ttk.Label(self.daily_forecast_frame, text=temp_label).grid(row=index, column=1, padx=5, pady=5, sticky="w")

        
            ttk.Label(self.daily_forecast_frame, text=forecast['description']).grid(row=index, column=2, padx=5, pady=5, sticky="w")
         

    def process_daily_forecast(self, forecast_data):
        daily_forecasts = {}
        for item in forecast_data['list']:
            date = datetime.datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            if date not in daily_forecasts:
                daily_forecasts[date] = {
                    'max_temp': item['main']['temp_max'],
                    'min_temp': item['main']['temp_min'],
                    'description': item['weather'][0]['description']
                }
            else:
                daily_forecasts[date]['max_temp'] = max(daily_forecasts[date]['max_temp'], item['main']['temp_max'])
                daily_forecasts[date]['min_temp'] = min(daily_forecasts[date]['min_temp'], item['main']['temp_min'])
                
                daily_forecasts[date]['description'] = item['weather'][0]['description']
        return daily_forecasts

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()