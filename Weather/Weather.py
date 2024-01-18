import tkinter as tk
from tkinter import ttk
import requests
import matplotlib.pyplot as plt

def fetch_weather(city):
    api_key = "0bdb263ccdd84296dc6a57e50fbcd336"  
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

def fetch_forecast(city):
    api_key = "0bdb263ccdd84296dc6a57e50fbcd336"  
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

def display_weather(data):
    weather_str = f"Weather in {data['name']}:\n\n"
    weather_str += f"Temperature: {data['main']['temp']}°F\n"
    weather_str += f"Description: {data['weather'][0]['description']}\n"
    weather_str += f"Humidity: {data['main']['humidity']}%\n"
    weather_str += f"Pressure: {data['main']['pressure']} hPa\n"
    weather_str += f"Wind Speed: {data['wind']['speed']} meter/sec\n"
    return weather_str

def display_forecast(data):
    forecast_str = "Forecast:\n"
    for forecast in data['list']:
        forecast_str += f"\nDate: {forecast['dt_txt']}\n"
        forecast_str += f"Temperature: {forecast['main']['temp']}°F\n"
        forecast_str += f"Description: {forecast['weather'][0]['description']}\n"
        forecast_str += f"Humidity: {forecast['main']['humidity']}%\n"
        forecast_str += f"Pressure: {forecast['main']['pressure']} hPa\n"
        forecast_str += f"Wind Speed: {forecast['wind']['speed']} meter/sec\n"
        forecast_str += "-" * 40 + "\n"
    return forecast_str

def plot_weather_forecast(data):
    dates = []
    temps = []

    for forecast in data['list']:
        dates.append(forecast['dt_txt'])
        temps.append(forecast['main']['temp'])

    plt.plot(dates, temps)
    plt.xlabel("Date")
    plt.ylabel("Temperature (°F)")
    plt.title(f"Weather Forecast")
    plt.xticks(rotation=45)
    plt.show()

def get_weather():
    city = city_combobox.get()
    weather_data = fetch_weather(city)
    weather_info = display_weather(weather_data)
    weather_display.config(text=weather_info)

def get_weather_forecast():
    city = city_combobox.get()
    forecast_data = fetch_forecast(city)
    forecast_info = display_forecast(forecast_data)
    weather_display.config(text=forecast_info)
    plot_weather_forecast(forecast_data)


window = tk.Tk()
window.title("Weather App")

city_label = tk.Label(window, text="Select City:")
city_label.pack()

city_combobox = ttk.Combobox(window)
city_combobox['values'] = ('London', 'New York', 'Paris', 'Tokyo', 'Istanbul', 'Izmir', 'Bali', 'Roma', 'Berlin', 'Hamburg', ) 
city_combobox.pack()

get_weather_button = tk.Button(window, text="Get Weather", command=get_weather)
get_weather_button.pack()

get_weather_forecast_button = tk.Button(window, text="Get Weather Forecast", command=get_weather_forecast)
get_weather_forecast_button.pack()

weather_display = tk.Label(window, text="")
weather_display.pack()

window.mainloop()