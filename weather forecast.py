import requests
import json
import time
import tkinter as tk
from tkinter import ttk

def get_weather(city):
    api_key = "e71f41462402ed8af85f57e58283926b"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city

    response = requests.get(complete_url)

    x = response.json()

    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"] - 273.15
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        lat = x['coord']['lat']
        lon = x['coord']['lon']
        output_text = " Temperature (in C unit) = " + str(current_temperature) + "\n atmospheric pressure (in hPa unit) = " + str(current_pressure) + "\n humidity (in percentage) = " + str(current_humidity) + "\n description = " + str(weather_description) + "\n latitude = " + str(lat) + "\n longitude = " + str(lon)

        # getting the forecast data
        forecast_base_url = "https://api.openweathermap.org/data/2.5/forecast?"
        forecast_url = forecast_base_url + "appid=" + api_key + "&q=" + city + "&units=metric"
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        # extracting the forecast for the next hour
        next_hour_forecast = forecast_data["list"][0]
        next_hour_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(next_hour_forecast['dt']))
        next_hour_precipitation = next_hour_forecast['pop']
        output_text += f"\nNext hour precipitation probability for {city} at {next_hour_time} is {next_hour_precipitation}%"

    else:
        output_text = "City Not Found"

    return output_text


def get_weather_btn_click():
    city = city_entry.get()
    weather_text = get_weather(city)
    output_text_label.config(text=weather_text)


# Create the main window and set its title
root = tk.Tk()
root.title("Weather App")

# Set the style of the window
style = ttk.Style()

# Set the background color of the window
style.configure("TFrame", background="#F5F5F5")

# Set the background and foreground colors of the labels and buttons
style.configure("TLabel", background="#F5F5F5", foreground="#606060")
style.configure("TButton", background="#FF0000", foreground="#FFFFFF")

# Set the background color of the entry box
style.map("TEntry", background=[("active", "#FFFFFF")])

# Create a label for the city input
city_label = ttk.Label(root, text="City:")
city_label.grid(column=0, row=0)

# Create an entry box for the city input
city_entry = ttk.Entry(root, width=30)
city_entry.grid(column=1, row=0)

# Create a button to get the weather
get_weather_btn = ttk.Button(root, text="Get Weather", command=get_weather_btn_click)
get_weather_btn.grid(column=2, row=0)

# Create a label for the output text
output_text_label = ttk.Label(root, text="")
output_text_label.grid(column=0, row=1, columnspan=3)

# Configure the style of the output text label
style.configure("TLabel", foreground="#212121", background="#f5f5f5", font=("Helvetica", 14), padding=10)

# Run the main loop
root.mainloop()
