"""
Weather Application using PySide6 and OpenWeather API.

This module defines a GUI-based weather application that allows users
to enter a location, select a temperature unit, and retrieve current
weather information using the OpenWeather API.

The API key is expected to be provided via the OPENWEATHER_API_KEY
environment variable.
"""

import sys
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QRadioButton,
    QButtonGroup,
    QGroupBox
)
import requests
import os

class WeatherApp(QWidget):
    def __init__(self):
        """
        Initialize the WeatherApp widget and set up the user interface.
        """
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        Set up and arrange all UI components.

        This includes input fields, radio buttons for unit selection,
        a button to fetch weather data, and a label to display results.
        """
        self.location_entry = QLineEdit(self)
        self.info_label = QLabel('', self)

        self.unit_group = QGroupBox("Select temperature unit:", self)
        self.unit_layout = QVBoxLayout(self)
        self.unit_btn_group = QButtonGroup(self)
        self.c_button = QRadioButton('Celsius', self)
        self.f_button = QRadioButton('Fahrenheit', self)
        self.k_button = QRadioButton('Kelvin', self)

        self.unit_btn_group.addButton(self.c_button, 1)
        self.unit_btn_group.addButton(self.f_button, 2)
        self.unit_btn_group.addButton(self.k_button, 3)

        self.unit_layout.addWidget(self.c_button)
        self.unit_layout.addWidget(self.f_button)
        self.unit_layout.addWidget(self.k_button)
        self.unit_group.setLayout(self.unit_layout)

        self.get_weather_btn = QPushButton('Get Weather', self)
        self.get_weather_btn.clicked.connect(self.get_weather_info)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Enter Location:', self))
        layout.addWidget(self.location_entry)
        layout.addWidget(self.unit_group)
        layout.addWidget(self.get_weather_btn)
        layout.addWidget(self.info_label)

        self.setLayout(layout)
        self.setWindowTitle('Weather App')
        self.show()

    def get_weather_info(self):
        """
        Retrieve weather data for the given location and update the UI.

        This method:
        - Reads the API key from the environment
        - Determines the selected temperature unit
        - Fetches weather data from the API
        - Displays formatted weather information or an error message
        """
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            raise RuntimeError("OPENWEATHER_API_KEY is not set")
        
        location = self.location_entry.text()
        unit = 'K'
        if self.c_button.isChecked():
            unit = 'C'
        elif self.f_button.isChecked():
            unit = 'F'

        weather_data = self.get_weather(api_key, location)
        if weather_data and "name" in weather_data:
            info = self.display_weather_info(weather_data, unit)
            self.info_label.setText(info)
        else:
            self.info_label.setText("Failed to fetch weather data. Please check the location and try again.")

    def get_weather(self, api_key, location):
        """
        Fetch weather data from the OpenWeather API.

        Parameters:
            api_key (str): The OpenWeather API key.
            location (str): The name of the location.

        Returns:
            dict: Parsed JSON response containing weather data.
        """
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
        response = requests.get(url)
        data = response.json()
        return data

    def display_weather_info(self, data, unit):
        """
        Format weather data into a readable string.

        Parameters:
            data (dict): Weather data returned by the API.
            unit (str): Temperature unit ('C', 'F', or 'K').

        Returns:
            str: A formatted string containing weather details.
        """
        location = data["name"]
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        if unit == "C":
            temperature = temperature - 273.15
            feels_like = feels_like - 273.15
            temp_min = temp_min - 273.15
            temp_max = temp_max - 273.15
            unit_label = "°C"
        elif unit == "F":
            temperature = (temperature - 273.15) * 9/5 + 32
            feels_like = (feels_like - 273.15) * 9/5 + 32
            temp_min = (temp_min - 273.15) * 9/5 + 32
            temp_max = (temp_max - 273.15) * 9/5 + 32
            unit_label = "°F"
        else:
            unit_label = "K"

        info = (
            f"Weather Information:\n"
            f"Location: {location}\n"
            f"Weather: {weather_description}\n"
            f"Temperature: {temperature:.2f} {unit_label}\n"
            f"Feels Like: {feels_like:.2f} {unit_label}\n"
            f"Min Temperature: {temp_min:.2f} {unit_label}\n"
            f"Max Temperature: {temp_max:.2f} {unit_label}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )
        return info


app = QApplication(sys.argv)
window = WeatherApp()
sys.exit(app.exec_())