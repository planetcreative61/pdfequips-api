import tempfile
from flask import jsonify, request, send_file
from utils.utils import validate_file
from tools.compress_pdf_tool import compress_pdf
import os

"""
    i want to delete the file and the compressed file if i finished compression and returned the file for the user to download
    i.e after the return statemet of the compress_pdf_handler if it's possible.
    is it possible to do this in a finally block for example?
"""


def compress_pdf_route(app):
    @app.route('/compress-pdf', methods=['POST'])
    def compress_pdf_handler():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        file = request.files.getlist("files")[0]
        error = validate_file(file)
        compressed_file = None
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        temp_file = tempfile.NamedTemporaryFile()
        file.save(temp_file.name)
        try:
            compressed_file = compress_pdf(temp_file.name)
            return send_file(compressed_file, download_name='compressed.pdf', as_attachment=True)
        except FileNotFoundError as err:
            return jsonify({"error": str(err)}), 404
        except ValueError as err:
            return jsonify({"error": str(err)}), 400
        finally:
            # Delete the original PDF file
            print(file.filename, compressed_file)
            if file.filename is not None and os.path.exists(file.filename):
                os.remove(file.filename)

            # Delete the compressed PDF file
            # this is not removing the compressed_file i want to delete it.
            if compressed_file is not None:
                os.remove(compressed_file)
