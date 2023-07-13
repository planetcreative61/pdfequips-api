from flask import jsonify, request
from utils.utils import validate_file
from pdf2wordconverter import pdf_to_word_converter, pdf_to_word_converter_multiple



def pdf_to_word_route(app):
    @app.route('/pdf-to-word', methods=['POST'])
    def convert_pdf_to_word():
        if 'files' not in request.files:
            return jsonify({"error": "No pdf_file found"}), 400
        files = request.files.getlist('files')
        error = validate_file(files)

        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        if len(files) == 1:
            pdf_file = files
            return pdf_to_word_converter(pdf_file[0])
        else:
            # this is not tested.
            return pdf_to_word_converter_multiple(files)
