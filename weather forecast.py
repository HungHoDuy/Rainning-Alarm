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

            print(f"Forecast data for {city}:")
            print(f"Time: {next_hour_time}")
            print(f"Rain probability: {next_hour_precipitation}")

            return next_hour_precipitation >= 50
        except (requests.exceptions.RequestException, ValueError):
            print(f"Unable to get forecast data for {city}")
            return False

    def check_rain_probability(self, city):
        def check_loop():
            while True:
                rain_probability = self.get_rain_probability(city)
                if rain_probability:
                    messagebox.showwarning("Rain Alert",
                                           f"There's a greater than or equal to 50% chance of rain in {city} in the next hour.")
                    break
                else:
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

#root = tk.Tk()
root.geometry("750x450")
root.title("Todo App")
root.configure(background="#36393F")

title_label = ttk.Label(root, text="Daily Tasks", foreground="#FFFFFF", background="#36393F", font=("Whitney", 30, "bold"))
title_label.pack(padx=10, pady=(40, 20))

scrollable_frame = ttk.Frame(root)
scrollable_frame.pack(pady=10)

canvas = tk.Canvas(scrollable_frame)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

scrollable_frame.interior = ttk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame.interior, anchor="nw")

entry = ttk.Entry(root, width=40, font=("Whitney", 12))
entry.pack(padx=10, pady=10, fill="x")

add_button = ttk.Button(root, text="Add", width=10, command=add_todo)
add_button.pack(pady=10)

# Set the style of the scrollbar
style = ttk.Style()
style.configure("Vertical.TScrollbar", background="#2C2F33")

# Run the main loop
root.mainloop()
