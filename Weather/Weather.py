import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime, timezone

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
    weather_str += f"Max Temperature: {data['main']['temp_max']}°F\n"  
    weather_str += f"Min Temperature: {data['main']['temp_min']}°F\n"  
    return weather_str

def display_forecast(data):
    forecast_str = "Forecast:\n"
    previous_date = None
    for forecast in data['list']:
        dt_txt = datetime.fromtimestamp(forecast['dt'], tz=timezone.utc)
        dt_txt_str = dt_txt.strftime('%Y-%m-%d')
        if dt_txt_str != previous_date:
            forecast_str += f"\nDate: {dt_txt_str}\n"
            forecast_str += f"Temperature: {forecast['main']['temp']}°F\n"
            forecast_str += f"Description: {forecast['weather'][0]['description']}\n"
            forecast_str += f"Humidity: {forecast['main']['humidity']}%\n"
            forecast_str += f"Pressure: {forecast['main']['pressure']} hPa\n"
            forecast_str += f"Wind Speed: {forecast['wind']['speed']} meter/sec\n"
            forecast_str += f"Max Temperature: {forecast['main']['temp_max']}°F\n"  
            forecast_str += f"Min Temperature: {forecast['main']['temp_min']}°F\n"  
            forecast_str += "-" * 40 + "\n"
            previous_date = dt_txt_str
    return forecast_str

def get_weather():
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    weather_display.config(text=current_datetime)
    city = city_entry.get()
    if city:
        weather_data = fetch_weather(city)
        weather_info = display_weather(weather_data)
        weather_display.config(text=weather_info)
    else:
        messagebox.showinfo("Error", "Please enter a city")

def get_weather_forecast():
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    weather_display.config(text=current_datetime)
    city = city_entry.get()
    if city:
        forecast_data = fetch_forecast(city)
        forecast_info = display_forecast(forecast_data)
        weather_display.config(text=forecast_info)
    else:
        messagebox.showinfo("Error", "Please enter a city")

window = tk.Tk()
window.title("Weather App")
window.style = ttk.Style()
window.style.theme_use("clam")

frame = ttk.Frame(window, padding=10)
frame.pack()

city_label = ttk.Label(frame, text="Enter City:")
city_label.pack(side="left")

city_entry = ttk.Entry(frame)
city_entry.pack(side="left", padx=5)

get_weather_button = ttk.Button(window, text="Get Weather", command=get_weather)
get_weather_button.pack(pady=5)

def new_func1(get_weather_forecast, window):
    get_weather_forecast_button = ttk.Button(window, text="Get Weather Forecast", command=get_weather_forecast)
    return get_weather_forecast_button

def new_func2(get_weather_forecast, window, new_func1):
    get_weather_forecast_button = new_func1(get_weather_forecast, window)
    return get_weather_forecast_button

get_weather_forecast_button = new_func2(get_weather_forecast, window, new_func1)
get_weather_forecast_button.pack(pady=5)

weather_display = ttk.Label(window, text="", justify="left")
weather_display.pack(pady=10)

def new_func(window):
    window.mainloop()

new_func(window)