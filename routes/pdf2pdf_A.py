from flask import jsonify, request
from utils.utils import validate_file
from pdf2pdfA_converter import pdf_to_pdfa


def pdf_to_pdfa_route(app):
    @app.route('/api/pdf-to-pdf-a', methods=['POST'])
    def pdf_to_pdfa_handler():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        files = request.files.getlist('files')
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        pdf_files = files
        return pdf_to_pdfa(pdf_files[0])
