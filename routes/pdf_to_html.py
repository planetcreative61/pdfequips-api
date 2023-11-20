import os
import shutil
from flask import request, jsonify, send_file, after_this_request
from utils.utils import validate_file
import json
from tools.pdf_to_html import pdf_to_html, pdf_to_html_multiple  # Assuming pdf_to_html functions exist

def pdf_to_html_route(app):
    @app.route('/api/pdf-to-html', methods=['POST'])
    def pdf_to_html_file():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        files = request.files.getlist('files')
        error = validate_file(files)
        if error:
            response = jsonify(error)
            response.headers['Content-Type'] = 'application/json'
            return jsonify({"error": response}), 400
        if len(files) == 1:
            # Call the pdf_to_html function with the files
            result = pdf_to_html(files[0])
            # Check the file extension of the result
            if result.endswith('.html'):
            # If the result is an HTML file, return it as a response
                response = send_file(result, mimetype='text/html',
                                    as_attachment=True, download_name='converted.html', conditional=True)
            elif result.endswith('.zip'):
                # If the result is a ZIP file, return it as a response
                response = send_file(result, mimetype='application/zip',
                                    as_attachment=True, download_name='converted.zip', conditional=True)

            return response

            @after_this_request
            def remove_file(response):
                os.remove(result)
                return response
            response.headers['X-Accel-Buffering'] = 'no'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Connection'] = 'close'
            return response
        # else:
        #     # Call the function with the files
        #     zip_file, temp_directory = pdf_to_html_multiple(
        #         files)
        #     # Return the zip_file as a response
        #     response = send_file(zip_file, mimetype='application/zip',
        #                          as_attachment=True, download_name='output.zip', conditional=True)
        #     response.headers['X-Accel-Buffering'] = 'no'
        #     response.headers['Cache-Control'] = 'no-cache'
        #     response.headers['Connection'] = 'close'

        #     @after_this_request
        #     def remove_file(response):
        #         os.remove(zip_file)
        #         shutil.rmtree(temp_directory)
        #         return response

        #     return response
