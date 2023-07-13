from flask import request, jsonify
from html2pdf_converter import html_to_pdf, html_to_pdf_multiple
from utils.utils import validate_file

def html_to_pdf_route(app):
    @app.route('/html-to-pdf', methods=['POST'])
    def convert_html_to_pdf():
        files = request.files.getlist("files")
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        if len(files) == 1:
            return html_to_pdf(files[0])
        else:
            return html_to_pdf_multiple(files)
