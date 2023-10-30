"""
    give me the implementation of this function, file is a flask file object which needs to be stored in a tmp folder before processing, and options is the settings options for how to style the numbers on the pdf file and it's defined as follows:
    options: {
        margin: "small" |
        "recommended" |
        "big",
        bulletPosition: string;
        font: string;
        startPage: number;
        rangeToNumber: { start: number; end: number };
        text: string;
        fontSize: number;
        documentLanguage: string;
        isBold: boolean;
        isItalic: boolean;
        isUnderlined: boolean;
        color: string;
        firstPageIsCover: boolean;
  }

  explanation:
  margin represents the margin, possible values "small" | "recommended" | "big"
  bulletPosition represents where to position the number in the pdf file page, possible values: ("top" | "bottom") + "left" | "center" | "right". for example: "top left", "bottom center"
  font: string representing font family, example: "Arial".
  startPage: number representing where to start numbering.
  rangeToNumber: object representing the range to number start from the from property and end in the end property.
  text: string representing string to insert for page number for example page 1, page 2, possible values:
  'insert only page number (recommended)',
  'page {n}',
  'page {n} of {x}',
  'Custom' <any>,
  if(text === 'insert only page number (recommended)') {
    insert only page number instead and don't add any additional text
  } else if(text === 'page {n}') {
    insert 'page {n}', and replace {n} with the page number
  } else if(text === 'page {n} of {x}') {
    n represents page number and x or total represents the total page count.
  } else {
    i.e if they inserted custom text: insert the custom text but {n} represents current page number and {x} or {total} represents the total pageCount.
  }
  fontSize represents the font size of the page number.
  documentLanguage represents the pdf language helps to set the numbering type of the document for example if it's set to "en" then use the 0-9 numbers, but if it's set to "ar" then use the ٠-٩ numbers and so on.
  isBold: boolean (true | false) whether or not to make the number bold.
  isItalic: boolean (true | false) whether or not to make the number italic.
  isUnderlined: boolean (true | false) whether or not to make the number underline.
  color: color of the page number.
  firstPageIsCover: boolean (true | false) whether or not to make the first page cover page.
"""


import tempfile
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import os
"""
    Traceback (most recent call last):
  File "/workspace/.pyenv_mirror/user/current/lib/python3.12/site-packages/reportlab/pdfbase/pdfmetrics.py", line 697, in getFont
    return _fonts[fontName]
           ^^^^^^^^^^^^^^^^
KeyError: 'arial'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/workspace/.pyenv_mirror/user/current/lib/python3.12/site-packages/flask/app.py", line 1478, in __call__
    return self.wsgi_app(environ, start_response)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/.pyenv_mirror/user/current/lib/python3.12/site-packages/flask/app.py", line 1458, in wsgi_app
    response = self.handle_exception(e)
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/.pyenv_mirror/user/current/lib/python3.12/site-packages/flask_cors/extension.py", line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
                                                ^^^^^^^^^^^^^^^^^^^^
  File "/workspace/.pyenv_mirror/user/current/lib/python3.12/site-packages/flask/app.py", line 1455, in wsgi_app
    response = self.full_dispatch_request()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/.pyenv_mirror/user/current/lib/python3.12/site-packages/flask/app.py", line 869, in full_dispatch_request
    rv = self.handle_user_exception(e)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/.pyenv_mirror/user/current/lib/python3.12/site-packages/flask_cors/extension.py", line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
                                                ^^^^^^^^^^^^^^^^^^^^
  File "/workspace/.pyenv_mirror/user/current/lib/python3.12/site-packages/flask/app.py", line 867, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/.pyenv_mirror/user/current/lib/python3.12/site-packages/flask/app.py", line 852, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/pdfequips-api/routes/number_pdf.py", line 25, in number_pdf_file
    result = number_pdf(files[0], options)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/pdfequips-api/tools/number_pdf.py", line 94, in number_pdf
    can.setFont(font, font_size)
  File "/workspace/.pyenv_mirror/user/current/lib/python3.12/site-packages/reportlab/pdfgen/canvas.py", line 1726, in setFont
    font = pdfmetrics.getFont(self._fontname)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/.pyenv_mirror/user/current/lib/python3.12/site-packages/reportlab/pdfbase/pdfmetrics.py", line 699, in getFont
    return findFontAndRegister(fontName)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/.pyenv_mirror/user/current/lib/python3.12/site-packages/reportlab/pdfbase/pdfmetrics.py", line 681, in findFontAndRegister
    face = getTypeFace(fontName)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/.pyenv_mirror/user/current/lib/python3.12/site-packages/reportlab/pdfbase/pdfmetrics.py", line 638, in getTypeFace
    return _typefaces[faceName]
           ^^^^^^^^^^^^^^^^^^^^
KeyError: 'arial'
"""
def number_pdf(file, options):
    # Store the file in a temporary folder before processing
    temp_folder = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_folder, file.filename)
    file.save(temp_file_path)

    # Extract the options
    margin = options.get('margin')
    bullet_position = options.get('bulletPosition')
    font = options.get('font')
    start_page = options.get('startPage')
    range_to_number = options.get('rangeToNumber')
    text = options.get('text')
    font_size = options.get('fontSize')
    document_language = options.get('documentLanguage')
    is_bold = options.get('isBold')
    is_italic = options.get('isItalic')
    is_underlined = options.get('isUnderlined')
    color = options.get('color')
    first_page_is_cover = options.get('firstPageIsCover')

    # Open the PDF file
    with open(temp_file_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        total_pages = len(pdf_reader.pages)

        # Create a new PDF writer
        pdf_writer = PdfWriter()

        # Iterate over each page in the PDF file
        for page_number in range(total_pages):
            # Create a new canvas for the page
            packet = tempfile.NamedTemporaryFile(delete=False)
            can = canvas.Canvas(packet, pagesize=letter)

            # Set the font properties
            # can.setFont(font, font_size)
            # if is_bold:
            #     can.setFont(font, font_size, 'bold')
            # if is_italic:
            #     can.setFont(font, font_size, 'italic')
            # if is_underlined:
            #     can.setFont(font, font_size, 'underline')

            # Set the color
            can.setFillColor(HexColor(color))

            # Calculate the page number based on the options
            if text == 'insert only page number (recommended)':
                page_text = str(start_page + page_number)
            elif text == 'page {n}':
                page_text = 'page {n}'.format(n=start_page + page_number)
            elif text == 'page {n} of {x}':
                page_text = 'page {n} of {x}'.format(n=start_page + page_number, x=total_pages)
            else:
                page_text = text.replace('{n}', str(start_page + page_number)).replace('{x}', str(total_pages))

            # Calculate the position of the page number
            if bullet_position.startswith('top'):
                y = letter[1] - (0.5 * inch)
            elif bullet_position.startswith('bottom'):
                y = 0.5 * inch

            if bullet_position.endswith('left'):
                x = 0.5 * inch
            elif bullet_position.endswith('center'):
                x = letter[0] / 2
            elif bullet_position.endswith('right'):
                x = letter[0] - (0.5 * inch)

            # Draw the page number on the canvas
            can.drawString(x, y, page_text)
            can.save()

            # Move the canvas to the beginning of the packet
            packet.seek(0)

            # Merge the canvas with the original page
            overlay = PdfReader(packet)
            page = pdf_reader.pages[page_number]
            page.merge_page(overlay.pages[0])

            # Add the modified page to the PDF writer
            pdf_writer.add_page(page)

    # Save the processed PDF to a new file
    processed_file_path = os.path.join(temp_folder, 'numbered.pdf')
    with open(processed_file_path, 'wb') as output_file:
        pdf_writer.write(output_file)

    # Return the processed file path
    return processed_file_path
