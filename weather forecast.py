import tkinter as tk
import tkinter.messagebox as messagebox
import threading
import requests
import json
import time


class RainProbabilityApp:

    def __init__(self, master):
        self.master = master
        self.master.geometry("750x450")
        self.master.title("Rain Probability Checker")

        self.title_label = tk.Label(self.master, text="Rain Probability Checker", font=("Helvetica", 30, "bold"))
        self.title_label.pack(padx=10, pady=(40, 20))

        self.input_frame = tk.Frame(self.master)
        self.input_frame.pack(pady=20)

        self.city_label = tk.Label(self.input_frame, text="City: ")
        self.city_label.pack(side=tk.LEFT)

        self.city_entry = tk.Entry(self.input_frame, width=50)
        self.city_entry.pack(side=tk.LEFT)

        self.check_button = tk.Button(self.input_frame, text="Check", bg="#7289DA", fg="#FFFFFF",
                                      command=self.get_weather_btn_click)

        self.check_button.pack(side=tk.LEFT, padx=10)
        self.status_label = tk.Label(self.input_frame, text="", fg="blue")
        self.status_label.pack(side=tk.LEFT, padx=10)

        self.forecast_label = tk.Label(self.input_frame, text="")
        self.forecast_label.pack(side=tk.LEFT, padx=10)


    def get_rain_probability(self, city):
        api_key = "e71f41462402ed8af85f57e58283926b"

        # Checking if the city exists
        check_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        check_response = requests.get(check_url)
        if check_response.status_code == 404:
            messagebox.showwarning("City Not Found", f"City '{city}' not found.")
            return False

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

            self.forecast_label.config(
                text=f"Forecast data for {city}:\nTime: {next_hour_time}\nRain probability: {next_hour_precipitation}%")
            self.forecast_label.pack(side=tk.LEFT, padx=10)

            return next_hour_precipitation >= 50, {"time": next_hour_time, "precipitation": next_hour_precipitation}
        except (requests.exceptions.RequestException, ValueError):
            print(f"Unable to get forecast data for {city}")
            return False

    def check_rain_probability(self, city):
        self.city_entry.config(state=tk.DISABLED)

        def check_loop():
            while True:
                rain_probability, forecast_data = self.get_rain_probability(city)
                if rain_probability:
                    self.status_label.config(
                        text=f"There's a greater than or equal to 50% chance of rain in {city} in the next hour.")
                    messagebox.showwarning("Rain Alert",
                                           f"There's a greater than or equal to 50% chance of rain in {city} in the next hour.")
                    break
                else:
                    self.status_label.config(text="Checking...")
                    self.forecast_label.config(
                        text=f"Forecast data for {city}:\nTime: {forecast_data['time']}\nRain probability: {forecast_data['precipitation']}")
                    time.sleep(600)

        t = threading.Thread(target=check_loop)
        t.start()

    def get_weather_btn_click(self):
        city = self.city_entry.get()
        self.check_rain_probability(city)


if __name__ == "__main__":
    root = tk.Tk()
    app = RainProbabilityApp(root)
    root.mainloop()
