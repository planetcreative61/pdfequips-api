"""
    please update this function to use the libretranslatepy to translate the passed flask file object from the from language to the to language
    also keep in mind that the passed flask object might need to be stored in a tmp folder before processing.
"""
import os
import tempfile
from PyPDF2 import PdfFileReader
from reportlab.pdfgen import canvas
from libretranslate import LibreTranslatePy

def translate_pdf(pdf, from_lang, to_lang):
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save the PDF file to the temporary directory
        pdf_path = os.path.join(temp_dir, 'input.pdf')
        pdf.save(pdf_path)

        # Extract text from PDF
        with open(pdf_path, 'rb') as f:
            reader = PdfFileReader(f)
            contents = reader.getPage(0).extractText()

        # Translate the text
        lt = LibreTranslatePy()
        translated = lt.translate(contents, from_lang, to_lang)

        # Create new PDF with translated text
        translated_pdf_path = os.path.join(temp_dir, 'translated.pdf')
        c = canvas.Canvas(translated_pdf_path)
        c.drawString(100, 750, translated)
        c.save()

    return translated_pdf_path
