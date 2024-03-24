from flask import Flask, render_template
from flask_qrcode import QRcode
from dotenv import load_dotenv
import os

from functions.projects.weather import weatherApp
from functions.projects.qrcode import qrcodeApp
from functions.projects.ocr import ocrApp

# Load environment variables
load_dotenv()

# Flask app initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
qrcode = QRcode(app)

# Projects landing page
@app.route('/',methods=["GET","POST"])
@app.route('/projects',methods=["GET","POST"])
def projects():
        return render_template('projects.html')

# Weather App
weather_api_key = os.getenv('WEATHER_API_KEY')
weatherApp(app, weather_api_key)

# QRCode App
qrcodeApp(app, qrcode)

# OCR App
ocrApp(app)

if __name__ == '__main__':
        app.run(debug=True, host="localhost", port=8080)
