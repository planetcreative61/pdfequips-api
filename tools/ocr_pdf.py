from pdf2image import convert_from_path
import io
import os
import tempfile
import pytesseract

def ocr_pdf(file, selectedLanguages):
 # Save the file object to a temporary file
 temp_file_path = os.path.join(tempfile.gettempdir(), 'temp.pdf')
 file.save(temp_file_path)
 # Convert the PDF to an image for OCR
 images = convert_from_path(temp_file_path)
 text = ''
 for image in images:
    # Check if selectedLanguages contains any None values
    if None in selectedLanguages:
        selectedLanguages.remove(None)
    text += pytesseract.image_to_string(image, lang='+'.join(selectedLanguages))
 # Save the OCR result to a new PDF file
 result_file_path = os.path.join(tempfile.gettempdir(), 'ocr_result.pdf')
 with open(result_file_path, 'w') as f:
    f.write(text)
 return result_file_path
