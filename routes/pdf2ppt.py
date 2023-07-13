from flask import jsonify, request
from utils.utils import validate_file
from pdf2pptx_converter import pdf_to_pptx, pdf_to_pptx_multiple


def pdf_to_ppt_route(app):
    @app.route('/pdf-to-powerpoint', methods=['POST'])
    def pdf_to_pptx_handler():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        files = request.files.getlist('files')
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        if len(files) == 1:
            return pdf_to_pptx(files[0]) # type: ignore
        else:
            return pdf_to_pptx_multiple(files)
