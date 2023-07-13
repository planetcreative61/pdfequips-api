from flask import request, jsonify
from utils.utils import validate_file

from word2pdfconverter import word_to_pdf, word_to_pdf_multiple




def word_to_pdf_route(app):
    @app.route('/word-to-pdf', methods=['POST'])
    def convert_word_to_pdf():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        files = request.files.getlist('files')
        if not files:
            return jsonify({"error": "No files provided"}), 400
        
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400

        if len(files) == 1:
           return word_to_pdf(files)
        else:
            return word_to_pdf_multiple(files)


