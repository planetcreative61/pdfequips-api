import io
from PIL import Image
from PyPDF2 import PdfMerger
from flask import jsonify, send_file


def is_valid_jpeg(image_file):
    try:
        Image.open(image_file)
    except IOError:
        return False
    return True



"""
    this function is returning a pdf file, but it's blank i.e white completely.
    it has a size, bt
"""
def image_to_pdf(images):
    merger = PdfMerger()
    for image in images:
        if not is_valid_jpeg(image):
            return jsonify({"error": "Invalid image format"}), 400

        image = Image.open(image)
        pdf_bytes = io.BytesIO()
        image.save(pdf_bytes, 'PDF')
        merger.append(pdf_bytes)

    final_pdf = io.BytesIO()
    merger.write(final_pdf)
    final_pdf.seek(0)

    return send_file(final_pdf, download_name='output.pdf',
                     as_attachment=True, mimetype='application/pdf')
