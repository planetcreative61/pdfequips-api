from flask import jsonify, request, send_file
from excel2pdf_converter import excel_to_pdf, excel_to_pdf_multiple
from utils.utils import validate_file



def excel_to_pdf_route(app):
    @app.route('/excel-to-pdf', methods=['POST'])
    def convert_excel_to_pdf():
        if 'files' not in request.files: # type: ignore
            return jsonify({"error": "No PDF file provided"}), 400
        files = request.files.getlist("files")
        error = validate_file(files)
        if error:
            print(error)
            return jsonify({"error": error}), 400
        if len(files) == 1:
            return excel_to_pdf(files)
        else:
            return excel_to_pdf_multiple(files)