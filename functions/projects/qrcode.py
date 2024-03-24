from flask import render_template, request, send_file, session
from PIL import Image
from pyzbar.pyzbar import decode
from werkzeug.utils import secure_filename

from functions.utils import image_allowed_file

class Error:
    def __init__(self, message, error):
        self.message = message
        self.error = error

def decode_qrcode(filename):
    decocdeQR = decode(Image.open(filename))
    return decocdeQR[0].data.decode('ascii')

def process_qrcode(file):
    if 'file' not in request.files or file.filename == '':
        return Error("No file selected!", "error")

    if not image_allowed_file(file.filename) or secure_filename(file.filename).lower().endswith(('.pdf', '.PDF')):
        return Error("Only bmp, jpg, jpeg, png, ppm, ras, sr, tif, and tiff extensions are allowed!", "error")

    filename = secure_filename(file.filename)
    session["decqrcode_file"] = filename
    file.save("./static/temp_db/" + filename)
    return Error('Successfully processed', "noError")

def qrcodeApp(app, qrcode):
    @app.route("/genqrcode", methods=["GET"])
    def run_generate():
        data = request.args.get("data", "")
        return send_file(qrcode(data, mode="raw", box_size=100, error_correction='H'), mimetype="image/png")

    @app.route('/decqrcode', methods=['POST', 'GET'])
    def run_decode():
        if request.method == "POST":
            file = request.files['file']
            result = process_qrcode(file)

            try:
                text = decode_qrcode("./static/temp_db/" + session["decqrcode_file"])
            except Exception as e:
                result = Error("Couldn't process your request", "error")
                text = ""

            return render_template('projects/qrcode.html',
                                   message = result.message,
                                   error = result.error,
                                   text = text,
                                   filename = "./static/temp_db/" + session.get("decqrcode_file", ""))

        return render_template('projects/qrcode.html',
                               text = "https://github.com/khalilrefai",
                               filename = "./static/img/my_github.png")
