from flask import request, jsonify
from img2pdfconverter import image_to_pdf
from utils.utils import validate_file
from flask import make_response


def jpg_to_pdf_route(app):
    @app.route('/api/jpg-to-pdf', methods=['POST'])
    def jpg_to_pdf_handler():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        files = request.files.getlist("files")
        print("FILES ARE => ", files)
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        images = request.files.getlist("files")
        response = make_response(image_to_pdf(images))
        response.headers.set('Content-Type', 'application/pdf')
        return response
