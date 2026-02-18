import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to fetch weather data from OpenWeatherMap API
def get_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Error fetching data: {response.status_code} - {response.text}")

# Function to parse forecast data for timestamps and temperatures
def parse_forecast_data(data):
    timestamps = []
    temperatures = []
    for entry in data['list']:
        dt = datetime.fromtimestamp(entry['dt'])
        temp = entry['main']['temp']
        timestamps.append(dt)
        temperatures.append(temp)
    return timestamps, temperatures

# Function to create and return a Matplotlib figure for temperature plot
def plot_weather(timestamps, temperatures, city):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(timestamps, temperatures, marker='o', linestyle='-', color='b')
    ax.set_title(f'Temperature Forecast for {city}')
    ax.set_xlabel('Date/Time')
    ax.set_ylabel('Temperature (°C)')
    ax.grid(True)
    ax.xaxis.set_major_formatter(DateFormatter('%m-%d %H:%M'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# Main Tkinter app class
class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenWeatherMap Visualizer")
        
        # API Key (replace with your actual key; use env vars for security)
        self.api_key = "0c021de7c555436fd411e62f45e17713"  # Replace this!
        
        # UI Elements
        self.city_label = tk.Label(root, text="Enter City:")
        self.city_label.pack(pady=5)
        self.city_entry = tk.Entry(root)
        self.city_entry.pack(pady=5)
        self.fetch_button = tk.Button(root, text="Fetch and Plot", command=self.fetch_and_plot)
        self.fetch_button.pack(pady=10)
        
        # Placeholder for Matplotlib canvas
        self.canvas = None
    
    def fetch_and_plot(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showerror("Error", "Please enter a city name.")
            return
        
        try:
            # Fetch and parse data
            data = get_weather_data(city, self.api_key)
            timestamps, temperatures = parse_forecast_data(data)
            
            # Generate plot
            fig = plot_weather(timestamps, temperatures, city)
            
            # Clear any previous plot
            if self.canvas:
                self.canvas.get_tk_widget().destroy()
            
            # Embed the plot in Tkinter
            self.canvas = FigureCanvasTkAgg(fig, master=self.root)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch or plot data: {str(e)}")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()



