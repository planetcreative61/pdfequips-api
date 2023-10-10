# from flask_cors import CORS
from flask import Flask

from routes.compresspdf_route import compress_pdf_route
from routes.excel2pdf import excel_to_pdf_route
from routes.extract_pages import extract_pages_route
from routes.html2pdf import html_to_pdf_route
from routes.img_2pdf import jpg_to_pdf_route
from routes.lock_pdf import lock_pdf_route
from routes.mergepdfs import merge_pdfs_route
from routes.pdf2excel import pdf_to_excel_route
from routes.pdf2img import pdf_to_jpg_route
from routes.pdf2pdf_A import pdf_to_pdfa_route
from routes.pdf2ppt import pdf_to_ppt_route
from routes.pdf2word import pdf_to_word_route
from routes.ppt2pdf import ppt_to_pdf_route
from routes.rotate_pdf import rotate_pdf_route
from routes.unlock_pdf import unlock_pdf_route
from routes.word2pdf import word_to_pdf_route
from routes.pdf2text import pdf_to_text_route
from routes.split_by_range import split_by_range_route
# from .utils import is_pdf, upload_file

# from compress_pdf import compress_pdf
# from werkzeug.utils import secure_filename

# from flask import abort

# only for DEVELOPMENT
import logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)


app = Flask(__name__)

# cors
# cors = CORS(app, resources={
#             r"/*": {"origins": ["http://149.100.159.150:3000"]}})

# cors = CORS(app)


# setting templates directory for get routes
# app.wsgi_app = ProxyFix(app.wsgi_app)
# app.jinja_loader = FileSystemLoader('/out')
# setting uploads folder


# converter routes
jpg_to_pdf_route(app)
pdf_to_jpg_route(app)
word_to_pdf_route(app)
pdf_to_word_route(app)
ppt_to_pdf_route(app)
html_to_pdf_route(app)
pdf_to_pdfa_route(app)
excel_to_pdf_route(app)
pdf_to_excel_route(app)
pdf_to_ppt_route(app)
compress_pdf_route(app)
pdf_to_text_route(app)
# other pdf tool routes
merge_pdfs_route(app)
lock_pdf_route(app)
unlock_pdf_route(app)
rotate_pdf_route(app)
split_by_range_route(app)
extract_pages_route(app)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000, use_reloader=True)
    # app.run(host='0.0.0.0', port=5000, debug=True)
