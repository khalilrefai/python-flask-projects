from flask import render_template, request, session
import cv2
import pytesseract
from werkzeug.utils import secure_filename

from functions.utils import image_allowed_file

class Error:
    def __init__(self, message, error):
        self.message = message
        self.error = error

pytesseract.pytesseract.tesseract_cmd = '/path/to/your/tesseract'
def extract_text(image, language):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, lang=language)
    return text

def ocrApp(app):
    @app.route('/ocr', methods=['POST', "GET"])
    def run_ocr():
        if request.method == "POST":
            file = request.files.get('file')
            language = request.form.get('language')
            result = Error("Successfully processed", "noError")

            if not file or file.filename == '':
                result = Error("No file selected!", "error")
            elif not image_allowed_file(file.filename) or secure_filename(file.filename).lower().endswith(('.pdf', '.PDF')):
                result = Error("Only bmp, jpg, jpeg, png, ppm, ras, sr, tif and tiff extensions are allowed!", "error")

            text = ""
            if result.error == "noError":
                session["ocr_file"] = secure_filename(file.filename)
                file_path = "./static/temp_db/" + session["ocr_file"]
                file.save(file_path)

                image = cv2.imread(file_path)
                if image is None:
                    result = Error("Error loading the image!", "error")

                text = extract_text(image, language)

                if 'ocr_file' not in session or not session["ocr_file"]:
                    result = Error("Error processing the image!", "error")

            return render_template('projects/ocr.html',
                                   message = result.message,
                                   error = result.error,
                                   text = text,
                                   filename = "./static/temp_db/"+ session["ocr_file"])

        return render_template('projects/ocr.html',
                               filename = "./static/img/image_to_text.png",
                               text = "Talk is CHEAP Show me the CODE")
