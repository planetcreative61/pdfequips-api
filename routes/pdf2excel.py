from flask import jsonify, request
from utils.utils import validate_file
from pdf2excel_converter import pdf_to_excel, pdf_to_excel_multiple

"""
    i want another function like this but for /pdf-to-text
"""


def pdf_to_excel_route(app):
    @app.route('/api/pdf-to-excel', methods=['POST'])
    def convert_pdf_to_excel():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        files = request.files.getlist('files')
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        files = request.files.getlist("files")
        if len(files) == 1:
            return pdf_to_excel(files)
        else:
            return pdf_to_excel_multiple(files)
