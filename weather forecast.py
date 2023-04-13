import requests
import json
import time
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import threading

def get_rain_probability(city):
    api_key = "e71f41462402ed8af85f57e58283926b"

    # Getting the forecast data
    forecast_base_url = "https://api.openweathermap.org/data/2.5/forecast?"
    forecast_url = forecast_base_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    try:
        forecast_response = requests.get(forecast_url, timeout=10)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        # Extracting the forecast for the next hour
        next_hour_forecast = forecast_data["list"][0]
        next_hour_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(next_hour_forecast['dt']))
        next_hour_precipitation = next_hour_forecast['pop'] * 100

        print(f"Forecast data for {city}:")
        print(f"Time: {next_hour_time}")
        print(f"Rain probability: {next_hour_precipitation}")

        return next_hour_precipitation >= 50
    except (requests.exceptions.RequestException, ValueError):
        print(f"Unable to get forecast data for {city}")
        return False


import threading


def check_rain_probability(city):
    def check_loop():
        while True:
            rain_probability = get_rain_probability(city)
            if rain_probability:
                messagebox.showwarning("Rain Alert",
                                       f"There's a greater than or equal to 50% chance of rain in {city} in the next hour.")
                break
            else:
                time.sleep(600)

    t = threading.Thread(target=check_loop)
    t.start()


def get_weather_btn_click():
    city = city_entry.get()
    check_rain_probability(city)


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
get_weather_btn = ttk.Button(root, text="Get Rain Probability", command=get_weather_btn_click)
get_weather_btn.grid(column=2, row=0)

# Create a label for the output text
output_text_label = ttk.Label(root, text="")
output_text_label.grid(column=0, row=1, columnspan=3)

# Configure the style of the output text label
style.configure("TLabel", foreground="#212121", background="#f5f5f5", font=("Helvetica", 14), padding=10)

# Run the main loop
root.mainloop()
