"""
    this is a pdf-to-markdown route handler, i want another similar function but for /api/pdf-to-html
    everything is the same except for the fuction used for the conversion i.e instead of pdf_to_markdown and pdf_to_markdown_multiple
    use pdf_to_html, pdf_to_html_multiple
"""

import os
import shutil
from flask import request, jsonify, send_file, after_this_request
from utils.utils import validate_file
import json
from tools.pdf_to_markdown import pdf_to_markdown, pdf_to_markdown_multiple

def pdf_to_markdown_route(app):
    @app.route('/api/pdf-to-markdown', methods=['POST'])
    def pdf_to_markdown_file():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        files = request.files.getlist('files')
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        if len(files) == 1:
            # Call the pdf_to_markdown function with the files
            result = pdf_to_markdown(files[0])
            # Return the result as a response
            response = send_file(result, mimetype='text/markdown',
                                 as_attachment=True, download_name='converted.md', conditional=True)

            @after_this_request
            def remove_file(response):
                os.remove(result)
                return response
            response.headers['X-Accel-Buffering'] = 'no'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Connection'] = 'close'
            return response
        else:
            # Call the function with the files
            zip_file, temp_directory = pdf_to_markdown_multiple(
                files)
            # Return the zip_file as a response
            response = send_file(zip_file, mimetype='application/zip',
                                 as_attachment=True, download_name='output.zip', conditional=True)
            response.headers['X-Accel-Buffering'] = 'no'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Connection'] = 'close'

            @after_this_request
            def remove_file(response):
                os.remove(zip_file)
                shutil.rmtree(temp_directory)
                return response

            return response

