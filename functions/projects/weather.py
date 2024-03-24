from flask import render_template, request
import urllib.request, urllib.parse, urllib.error
import json

class Error:
    def __init__(self, message, error):
        self.message = message
        self.error = error

def toCelcius(temp):
    return str(round(float(temp) - 273.16, 2))

def weatherApp(app, weather_api_key):
    @app.route('/weather', methods = ['POST', 'GET'])
    def run_weather():
        if request.method == 'POST':
            city = request.form['city']

            # source contains JSON data from API
            try:
                source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + 
                                                city + 
                                                '&appid=' + 
                                                weather_api_key).read()

                # Converting JSON data to dictionary
                list_of_data = json.loads(source)

                # Data
                data = {
                    "country_code": str(list_of_data['sys']['country']),
                    "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
                    "temp": str(list_of_data['main']['temp']) + 'k',
                    "temp_cel": toCelcius(list_of_data['main']['temp']) + ' °C',
                    "pressure": str(list_of_data['main']['pressure']) + ' mb',
                    "humidity": str(list_of_data['main']['humidity']) + '%',
                    "cityname": str(city),
                }

                result = Error("Successfully processed", "noError")
            except:
                data = {}
                result = Error("Couldn't process your request", "error")

            return render_template('projects/weather.html',
                                   data = data,
                                   message = result.message,
                                   error = result.error)

        return render_template('projects/weather.html')
