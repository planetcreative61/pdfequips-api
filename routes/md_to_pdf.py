import os
import shutil
from flask import jsonify, request, send_file, after_this_request
from tools.markdown_to_pdf import md_text_to_pdf, md_to_pdf, github_md_files_to_pdf
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
    @app.route("/api/markdown-to-pdf", methods=['POST'])
    def md_to_pdf_handler():
        files = request.files.getlist('files')
        selectedGithubMarkdownUrls = json.loads(request.form.get('selectedGithubMarkdownUrls'))

        if len(files) == 0 and len(selectedGithubMarkdownUrls) == 0:
            return jsonify({"error": "No Markdown files or GitHub URLs provided"}), 400

        if len(selectedGithubMarkdownUrls) > 0:
            pdf_path, tmp_path = github_md_files_to_pdf(selectedGithubMarkdownUrls)
        else:
            pdf_path, tmp_path = md_to_pdf(files)

        @after_this_request
        def remove_tmp_files(response):
            if os.path.isfile(tmp_path) and tmp_path.endswith('.md'):
                os.remove(tmp_path)
            else:
                shutil.rmtree(tmp_path)
            return response

        if tmp_path.endswith('.md'):
            return send_file(pdf_path, as_attachment=True)
        else:
            return send_file(pdf_path, as_attachment=True, download_name='output.zip')
