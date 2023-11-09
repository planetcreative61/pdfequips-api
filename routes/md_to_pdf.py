import os
import shutil
from flask import jsonify, request, send_file, after_this_request
from tools.markdown_to_pdf import md_text_to_pdf
from utils.utils import validate_file
import json

def md_text_to_pdf_route(app):
    @app.route("/api/md-text-to-pdf", methods=['POST'])
    def md_text_to_pdf_handler():
        md = json.loads(request.form.get('markdown'))
        md_file, pdf_path = md_text_to_pdf(md['markdown'])
        @after_this_request
        def remove_file(response):
            try:
                os.remove(pdf_path)
                os.remove(md_file)
            except Exception as error:
                app.logger.error("Error removing or closing downloaded file handle", error)
            return response

        return send_file(pdf_path, as_attachment=True, download_name="output.pdf")

def md_to_pdf_route(app):
    @app.route("/api/md-to-pdf", methods=['POST'])
    def md_to_pdf_handler():
        if 'files' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        files = request.files.getlist('files')
        if len(files) == 1:
            pdf_path = md_to_pdf(files[0])
            pass
        pass
