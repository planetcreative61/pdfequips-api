import tempfile
from flask import jsonify, request
from utils.utils import validate_file
from tools.merge_pdf_tool import merge_pdfs


def merge_pdfs_route(app):
    @app.route('/merge-pdf', methods=['POST'])
    def merge_pdfs_handler():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        files = request.files.getlist('files')
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        pdf_files = []
        for file in files:
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            file.save(temp_file.name)
            pdf_files.append(temp_file.name)
        try:
            merged_pdf = merge_pdfs(pdf_files)
            return merged_pdf
        except FileNotFoundError as err:
            return jsonify({"error": str(err)}), 404
        except TypeError as err:
            return jsonify({"error": str(err)}), 400
