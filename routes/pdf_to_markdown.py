import os
import shutil
from flask import request, jsonify, send_file, after_this_request
from utils.utils import validate_file
import json
from tools.pdf_to_markdown import pdf_to_markdown

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
            # Replace the following line with your actual implementation
            result = pdf_to_markdown(files[0])
            # Return the result as a response
            # Replace the following line with your actual implementation
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
