from flask import request, jsonify
from utils.utils import validate_file
from powerpoint2pdfconverter import ppt_to_pdf, ppt_to_pdf_multiple

def ppt_to_pdf_route(app):
    @app.route('/powerpoint-to-pdf', methods=['POST'])
    def convert_ppt_to_pdf():
        files = request.files.getlist('files')
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return response, 400
        if len(files) == 1:
            return ppt_to_pdf(files)
        else: 
            return ppt_to_pdf_multiple(files)

