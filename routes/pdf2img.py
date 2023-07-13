import os
from flask import jsonify, request
from utils.utils import validate_file
from pdf_to_jpg_converter import pdf_to_jpg_converter, pdf_to_jpg_converter_multiple


def pdf_to_jpg_route(app):
    # Define the route and function to handle the POST request
    @app.route('/pdf-to-jpg', methods=['POST'])
    def pdf_to_jpg_endpoint():
        if request.method == 'POST':
            # Create the temp directory if it doesn't exist
            if not os.path.exists('temp'):
                os.makedirs('temp')
            files = request.files.getlist('files')
            error = validate_file(files)
            if error:
                print("error => ", error)
                return jsonify({"error": error}), 400
            if len(files) == 1:
                return pdf_to_jpg_converter(files)
            else:
                return pdf_to_jpg_converter_multiple(files)
