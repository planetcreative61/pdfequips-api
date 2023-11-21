"""
    i have a java mvn project that is called number-pdf, i want to create a program that adds numbers to pdf files.
    the definition of the program:
    it's a java command line program that adds page numbers to pdf files,
    the java command line program would take two arguments, filePath and Options
    file path is the file path of the file to be processed,
    please provide the definition of the number_pdf function using python and i already have ghostscript installed and libreoffice so we can use one of them to create the function, the function is reciving two arguments:
    # file is a flask file object which needs to be stored in a tmp folder before processing,
    # and options is the settings options for how to style the numbers on the pdf file and it's defined as follows:
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
  }, default value(if user did'nt update the options object): {
    margin: "recommended",
    bulletPosition: "top left",
    font: "Arial",
    startPage: 0,
    rangeToNumber: { start: 1, end: <page-count of the pdf file> },
    text: "",
    fontSize: 12,
    documentLanguage: "en",
    isBold: true,
    isItalic: true,
    isUnderlined: true,
    color: "#000",
    firstPageIsCover: false,
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
  please keep in mind that the current implementation is based on gs which is not working i suggest using pdftk but use the best suited option available that satisfies these requirements.
  this java program is meant to be used on a python flask program as a service for a front-end.
  please give me the full implementation of the NumberPDF class
"""
# okay now please give me the complete code updated with the library you suggested, old code:
# import tempfile
# from PyPDF2 import PdfReader, PdfWriter
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# from reportlab.lib.units import inch
# from reportlab.lib.colors import HexColor
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont

# import os

# def number_pdf(file, options):
#   pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'))
#   pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))
#   pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
#   pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
#   pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'))

#   pdfmetrics.registerFont(TTFont('Arial', '/usr/share/fonts/truetype/msttcorefonts/Arial_Italic.ttf'))
#   pdfmetrics.registerFont(TTFont('Arial', '/usr/share/fonts/truetype/msttcorefonts/ariblk.ttf'))
#   pdfmetrics.registerFont(TTFont('Arial', '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf'))
#   pdfmetrics.registerFont(TTFont('Arial', '/usr/share/fonts/truetype/msttcorefonts/arialbd.ttf'))
#   pdfmetrics.registerFont(TTFont('Arial', '/usr/share/fonts/truetype/msttcorefonts/Arial_Bold_Italic.ttf'))
#   pdfmetrics.registerFont(TTFont('Arial', '/usr/share/fonts/truetype/msttcorefonts/arialbi.ttf'))
#   pdfmetrics.registerFont(TTFont('Arial', '/usr/share/fonts/truetype/msttcorefonts/Arial_Black.ttf'))
#   pdfmetrics.registerFont(TTFont('Arial', '/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf'))
#   pdfmetrics.registerFont(TTFont('Arial', '/usr/share/fonts/truetype/msttcorefonts/ariali.ttf'))

#   # Store the file in a temporary folder before processing
#   temp_folder = tempfile.mkdtemp()
#   temp_file_path = os.path.join(temp_folder, file.filename)
#   file.save(temp_file_path)

#   # Open the PDF file
#   with open(temp_file_path, 'rb') as pdf_file:
#       pdf_reader = PdfReader(pdf_file)
#       total_pages = len(pdf_reader.pages)

#       # Create a new PDF writer
#       pdf_writer = PdfWriter()

#       # Iterate over each page in the PDF file
#       for page_number in range(total_pages):
#           page = pdf_reader.pages[page_number]
#           modified_page = add_page_number(page, options, page_number, total_pages)
#           pdf_writer.add_page(modified_page)

#   # Save the processed PDF to a new file
#   processed_file_path = os.path.join(temp_folder, 'numbered.pdf')
#   with open(processed_file_path, 'wb') as output_file:
#       pdf_writer.write(output_file)

#   # Return the processed file path
#   return processed_file_path

# def add_page_number(page, options, page_number, total_pages):
#     # Extract the options
#     margin = options.get('margin')
#     bullet_position = options.get('bulletPosition')
#     font = options.get('font')
#     start_page = options.get('startPage')
#     range_to_number = options.get('rangeToNumber')
#     text = options.get('text')
#     font_size = options.get('fontSize')
#     document_language = options.get('documentLanguage')
#     is_bold = options.get('isBold')
#     is_italic = options.get('isItalic')
#     is_underlined = options.get('isUnderlined')
#     color = options.get('color')
#     first_page_is_cover = options.get('firstPageIsCover')

#     # Create a new canvas for the page
#     packet = tempfile.NamedTemporaryFile(delete=False)
#     can = canvas.Canvas(packet, pagesize=letter)

#     # Set the font properties
#     can.setFont(font, font_size)
#     if is_bold:
#         can.setFont(font, font_size, 'bold')
#     if is_italic:
#         can.setFont(font, font_size, 'italic')
#     if is_underlined:
#         can.setFont(font, font_size, 'underline')

#     # Set the color
#     can.setFillColor(HexColor(color))

#     # Calculate the page number based on the options
#     if text == 'insert only page number (recommended)':
#         page_text = str(start_page + page_number)
#     elif text == 'page {n}':
#         page_text = 'page {n}'.format(n=start_page + page_number)
#     elif text == 'page {n} of {x}':
#         page_text = 'page {n} of {x}'.format(n=start_page + page_number, x=total_pages)
#     else:
#         page_text = text.replace('{n}', str(start_page + page_number)).replace('{x}', str(total_pages))

#     # Calculate the position of the page number
#     if bullet_position.startswith('top'):
#         y = letter[1] - (0.5 * inch)
#     elif bullet_position.startswith('bottom'):
#         y = 0.5 * inch

#     if bullet_position.endswith('left'):
#         x = 0.5 * inch
#     elif bullet_position.endswith('center'):
#         x = letter[0] / 2
#     elif bullet_position.endswith('right'):
#         x = letter[0] - (0.5 * inch)

#     # Draw the page number on the canvas
#     print(type(x), type(y), page_text)
#     y = float(y)
#     x = float(x)
#     can.drawString(x, y, page_text)
#     can.save()

#     # Move the canvas to the beginning of the packet
#     packet.seek(0)

#     # Merge the canvas with the original page
#     overlay = PdfReader(packet)
#     modified_page = page.merge_page(overlay.pages[0])

#     return modified_page

# import tempfile
# import fitz
# import os

# def number_pdf(file, options):
#     # Store the file in a temporary folder before processing
#     temp_folder = tempfile.mkdtemp()
#     temp_file_path = os.path.join(temp_folder, file.filename)
#     file.save(temp_file_path)

#     # Open the PDF file
#     doc = fitz.open(temp_file_path)
#     total_pages = len(doc)

#     # Extract the options
#     font = options.get('font', 'helv')
#     font_size = options.get('fontSize', 12) if options.get('fontSize', 12) > 0 else 12
#     color = options.get('color', (0, 0, 0))
#     bullet_position = options.get('bulletPosition', 'top-left')
#     start_page = options.get('startPage', 1)
#     range_to_number = options.get('rangeToNumber', {'start': 1, 'end': total_pages})
#     text = options.get('text', 'Page {n}') if options.get('text', 'Page {n}') else 'Page {n}'
#     document_language = options.get('documentLanguage', 'en')
#     first_page_is_cover = options.get('firstPageIsCover', False)

#     # Calculate the position of the page number
#     if bullet_position.startswith('top'):
#         y = doc[0].rect.height - 20
#     elif bullet_position.startswith('bottom'):
#         y = 20

#     if bullet_position.endswith('left'):
#         x = 20
#     elif bullet_position.endswith('center'):
#         x = doc[0].rect.width / 2
#     elif bullet_position.endswith('right'):
#         x = doc[0].rect.width - 20

#     # Iterate over each page in the PDF file
#     for page_number in range(total_pages):
#         page = doc[page_number]

#         # Skip the first page if it's a cover page
#         if first_page_is_cover and page_number == 0:
#             continue

#         # Skip the page if it's not in the range to number
#         if not (range_to_number['start'] <= page_number + 1 <= range_to_number['end']):
#             continue

#         # Calculate the page number based on the options
#         if text == 'insert only page number (recommended)':
#             page_text = str(start_page + page_number)
#         else:
#             page_text = text.replace('{n}', str(start_page + page_number)).replace('{x}', str(total_pages))

#         # Convert the page number to Arabic numerals if the document language is Arabic
#         if document_language == 'ar':
#             page_text = page_text.translate(str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩'))

#         # Draw the page number on the page
#         page.insert_text((x, y), page_text, fontsize=font_size, fontname=font, color=color)

#     # Save the processed PDF to a new file
#     processed_file_path = os.path.join(temp_folder, 'numbered.pdf')
#     doc.save(processed_file_path)

#     # Return the processed file path
#     return processed_file_path

# import os
# import tempfile
# import PyPDF2
# import subprocess
# def number_pdf(file, options):
#   # # Step 1: Save the file in a temporary folder
#   # temp_dir = tempfile.mkdtemp()
#   # temp_file = os.path.join(temp_dir, file.filename)
#   # file.save(temp_file)
#   # print(options['color'])
#   # # Step 2: Get the total number of pages in the PDF file
#   # with open(temp_file, 'rb') as f:
#   #     pdf_reader = PyPDF2.PdfReader(f)
#   #     total_pages = len(pdf_reader.pages)

#   # # Step 3: Set default options if not provided by the user
#   # # default_options = {
#   # #     "margin": "recommended",
#   # #     "bulletPosition": "top left",
#   # #     "font": "Arial",
#   # #     "startPage": 0,
#   # #     "rangeToNumber": {"start": 1, "end": total_pages},
#   # #     "text": "",
#   # #     "fontSize": 12,
#   # #     "documentLanguage": "en",
#   # #     "isBold": True,
#   # #     "isItalic": True,
#   # #     "isUnderlined": True,
#   # #     "color": "#000",
#   # #     "firstPageIsCover": False
#   # # }
#   # options = {**default_options, **options}

#   # # Step 4: Generate the command for Ghostscript
#   # command = [
#   #     "gs",
#   #     "-o",
#   #     os.path.join(temp_dir, "numbered.pdf"),
#   #     "-sDEVICE=pdfwrite",
#   #     "-dPDFSETTINGS=/prepress",
#   #     "-dNOPAUSE",
#   #     "-dBATCH",
#   #     "-dSAFER",
#   #     "-dFirstPage={}".format(options["startPage"] + 1),
#   #     "-dLastPage={}".format(total_pages),
#   #     "-sOutputFile=-",
#   #     "-c",
#   #     "({}) /Helvetica findfont {} scalefont setfont".format(options["font"], options["fontSize"]),
#   #     "-c",
#   #     # "1 {} {} {} {} {} setrgbcolor".format(int(options["isBold"]), int(options["isItalic"]), int(options["isUnderlined"]), int(options["color"][1:3], 16), int(options["color"][3:5], 16), int(options["color"][5:7], 16)),
#   #     "1 {} {} {} {} {} setrgbcolor".format(int(options["isBold"]), int(options["isItalic"]), int(options["isUnderlined"]), int(options["color"][1:3], 16), int(options["color"][3:5], 16), int(options["color"][5:7], 16)),
#   #     "-c",
#   #     "/PageNum exch def",
#   #     "-c",
#   #     "/PageCount {} def".format(total_pages),
#   #     "-c",
#   #     "/Margin {} def".format(options["margin"]),
#   #     "-c",
#   #     "/BulletPosition ({}) def".format(options["bulletPosition"]),
#   #     "-c",
#   #     "/Text ({}) def".format(options["text"]),
#   #     "-c",
#   #     "/DocumentLanguage ({}) def".format(options["documentLanguage"]),
#   #     "-c",
#   #     "/FirstPageIsCover {} def".format(int(options["firstPageIsCover"])),
#   #     "-f",
#   #     temp_file,
#   #     "number_pages.ps"
#   # ]

#   # # Step 5: Run Ghostscript to add page numbers
#   # subprocess.run(command, capture_output=True)

#   # # Step 6: Return the path to the numbered PDF file
#   # numbered_pdf_path = os.path.join(temp_dir, "numbered.pdf")
#   # return numbered_pdf_path
#   # Step 1: Save the file in a temporary folder
#   temp_dir = tempfile.mkdtemp()
#   temp_file = os.path.join(temp_dir, file.filename)
#   file.save(temp_file)

#   # Step 2: Get the total number of pages in the PDF file
#   with open(temp_file, 'rb') as f:
#       pdf_reader = PyPDF2.PdfReader(f)
#       total_pages = len(pdf_reader.pages)

#   # Step 3: Set default options if not provided by the user
#   default_options = {
#       "margin": "recommended",
#       "bulletPosition": "top left",
#       "font": "Arial",
#       "startPage": 0,
#       "rangeToNumber": {"start": 1, "end": total_pages},
#       "text": "",
#       "fontSize": 12,
#       "documentLanguage": "en",
#       "isBold": True,
#       "isItalic": True,
#       "isUnderlined": True,
#       "color": "#00000000",
#       "firstPageIsCover": False
#   }
#   options = {**default_options, **options}

#   # Step 4: Generate the command for Ghostscript
#   command = [
#       "gs",
#       "-dDEBUG",
#       "-o",
#       os.path.join(temp_dir, "numbered.pdf"),
#       "-sDEVICE=pdfwrite",
#       "-dPDFSETTINGS=/prepress",
#       "-dNOPAUSE",
#       "-dBATCH",
#       "-dSAFER",
#       "-dFirstPage={}".format(options["startPage"] + 1),
#       "-dLastPage={}".format(total_pages),
#       "-sOutputFile=-",
#       "-c",
#       "({}) /Helvetica findfont {} scalefont setfont".format(options["font"], options["fontSize"]),
#       "-c",
#       # "1 {} {} {} {} {} setrgbcolor".format(int(options["isBold"]), int(options["isItalic"]), int(options["isUnderlined"]), int(options["color"][1:3], 16), int(options["color"][3:5], 16), int(options["color"][5:7], 16)),
#       "1 {} {} {} {} {} setrgbcolor".format(int(options["isBold"]), int(options["isItalic"]), int(options["isUnderlined"]), int(options["color"][1:3], 16), int(options["color"][3:5], 16), int(options["color"][5:7], 16)),
#       "-c",
#       "/PageNum exch def",
#       "-c",
#       "/PageCount {} def".format(total_pages),
#       "-c",
#       "/Margin {} def".format(options["margin"]),
#       "-c",
#       "/BulletPosition ({}) def".format(options["bulletPosition"]),
#       "-c",
#       "/Text ({}) def".format(options["text"]),
#       "-c",
#       "/DocumentLanguage ({}) def".format(options["documentLanguage"]),
#       "-c",
#       "/FirstPageIsCover {} def".format(int(options["firstPageIsCover"])),
#       "-f",
#       temp_file,
#       "number_pages.ps"
#   ]

#   # Step 5: Run Ghostscript to add page numbers
#   subprocess.run(command, capture_output=True)

#   # Step 6: Return the path to the numbered PDF file
#   numbered_pdf_path = os.path.join(temp_dir, "numbered.pdf")
#   return numbered_pdf_path



# import os
# import tempfile
# import subprocess
# import PyPDF2

# def number_pdf(file, options):
#     # Step 1: Save the file in a temporary folder
#     temp_dir = tempfile.mkdtemp()
#     temp_file = os.path.join(temp_dir, file.filename)
#     file.save(temp_file)

#     # Step 2: Get the total number of pages in the PDF file
#     with open(temp_file, 'rb') as f:
#         pdf_reader = PyPDF2.PdfReader(f)
#         total_pages = len(pdf_reader.pages)

#     # Step 3: Set default options if not provided by the user
#     default_options = {
#         "margin": "recommended",
#         "bulletPosition": "top left",
#         "font": "Arial",
#         "startPage": 0,
#         "rangeToNumber": {"start": 1, "end": total_pages},
#         "text": "",
#         "fontSize": 12,
#         "documentLanguage": "en",
#         "isBold": True,
#         "isItalic": True,
#         "isUnderlined": True,
#         "color": "#00000000",
#         "firstPageIsCover": False
#     }
#     options = {**default_options, **options}

#     # Step 4: Generate the command for Ghostscript
#     command = [
#         "gs",
#         "-dDEBUG",
#         "-o",
#         os.path.join(temp_dir, "numbered.pdf"),
#         "-sDEVICE=pdfwrite",
#         "-dPDFSETTINGS=/prepress",
#         "-dNOPAUSE",
#         "-dBATCH",
#         "-dSAFER",
#         "-dFirstPage={}".format(options["startPage"] + 1),
#         "-dLastPage={}".format(total_pages),
#         "-sOutputFile=-",
#         "-c",
#         "({}) /Helvetica findfont {} scalefont setfont".format(options["font"], options["fontSize"]),
#         "-c",
#         "1 {} {} {} {} {} setrgbcolor".format(
#             int(options["isBold"]),
#             int(options["isItalic"]),
#             int(options["isUnderlined"]),
#             int(options["color"][1:3], 16),
#             int(options["color"][3:5], 16),
#             int(options["color"][5:7], 16)
#         ),
#         "-c",
#         "/PageNum exch def",
#         "-c",
#         "/PageCount {} def".format(total_pages),
#         "-c",
#         "/Margin {} def".format(options["margin"]),
#         "-c",
#         "/BulletPosition ({}) def".format(options["bulletPosition"]),
#         "-c",
#         "/Text ({}) def".format(options["text"]),
#         "-c",
#         "/DocumentLanguage ({}) def".format(options["documentLanguage"]),
#         "-c",
#         "/FirstPageIsCover {} def".format(int(options["firstPageIsCover"])),
#         "-f",
#         temp_file,
#         "number_pages.ps"
#     ]

#     # Step 5: Run Ghostscript to add page numbers
#     subprocess.run(command, capture_output=True)

#     # Step 6: Return the path to the numbered PDF file
#     numbered_pdf_path = os.path.join(temp_dir, "numbered.pdf")
#     return numbered_pdf_path





# from PyPDF2 import PdfReader, PdfWriter
# from fpdf import FPDF
# from tempfile import TemporaryDirectory
# import os
# import shutil

# """
#   Traceback (most recent call last):
#   File "/workspace/pdfequips-api/.venv/lib/python3.10/site-packages/flask/app.py", line 2548, in __call__
#     return self.wsgi_app(environ, start_response)
#   File "/workspace/pdfequips-api/.venv/lib/python3.10/site-packages/flask/app.py", line 2528, in wsgi_app
#     response = self.handle_exception(e)
#   File "/workspace/pdfequips-api/.venv/lib/python3.10/site-packages/flask_cors/extension.py", line 176, in wrapped_function
#     return cors_after_request(app.make_response(f(*args, **kwargs)))
#   File "/workspace/pdfequips-api/.venv/lib/python3.10/site-packages/flask/app.py", line 2525, in wsgi_app
#     response = self.full_dispatch_request()
#   File "/workspace/pdfequips-api/.venv/lib/python3.10/site-packages/flask/app.py", line 1822, in full_dispatch_request
#     rv = self.handle_user_exception(e)
#   File "/workspace/pdfequips-api/.venv/lib/python3.10/site-packages/flask_cors/extension.py", line 176, in wrapped_function
#     return cors_after_request(app.make_response(f(*args, **kwargs)))
#   File "/workspace/pdfequips-api/.venv/lib/python3.10/site-packages/flask/app.py", line 1820, in full_dispatch_request
#     rv = self.dispatch_request()
#   File "/workspace/pdfequips-api/.venv/lib/python3.10/site-packages/flask/app.py", line 1796, in dispatch_request
#     return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
#   File "/workspace/pdfequips-api/routes/number_pdf.py", line 28, in number_pdf_file
#     response = send_file(result, mimetype='application/pdf',
#   File "/workspace/pdfequips-api/.venv/lib/python3.10/site-packages/flask/helpers.py", line 537, in send_file
#     return werkzeug.utils.send_file(  # type: ignore[return-value]
#   File "/workspace/pdfequips-api/.venv/lib/python3.10/site-packages/werkzeug/utils.py", line 440, in send_file
#     stat = os.stat(path)
# FileNotFoundError: [Errno 2] No such file or directory: '/tmp/tmpvmpo70_2/output.pdf'
# """
# def number_pdf(file, options=None):
#   # Define the default options
#   default_options = {
#       "margin": "recommended",
#       "bulletPosition": "top left",
#       "font": "Arial",
#       "startPage": 0,
#       "rangeToNumber": {"start": 1, "end": None},
#       "text": "",
#       "fontSize": 12,
#       "documentLanguage": "en",
#       "isBold": True,
#       "isItalic": True,
#       "isUnderlined": True,
#       "color": "#000",
#       "firstPageIsCover": False,
#   }

#   # Merge the user options with the default options
#   if options is not None:
#       default_options.update(options)
#   options = default_options

#   # Save the file to a temporary directory
#   with TemporaryDirectory() as tmpdirname:
#       file.save(os.path.join(tmpdirname, 'file.pdf'))

#       # Open the PDF file
#       reader = PdfReader(os.path.join(tmpdirname, 'file.pdf'))

#       # Get the total number of pages
#       total_pages = len(reader.pages)

#       # Update the end page if it's not set
#       if options["rangeToNumber"]["end"] is None:
#           options["rangeToNumber"]["end"] = total_pages

#       # Create a PdfWriter object
#       writer = PdfWriter()

#       # Iterate over all the pages in the PDF
#       for i in range(total_pages):
#           # Get the current page
#           page = reader.pages[i]

#           # Check if the current page is in the range to number
#           if i+1 >= options["rangeToNumber"]["start"] and i+1 <= options["rangeToNumber"]["end"]:
#               # Create a new FPDF object to overlay the page number
#               overlay = FPDF()
#               overlay.add_page()

#               # Set the options for the page number
#               overlay.set_font(options["font"], size=options["fontSize"])
#               overlay.set_text_color(0, 0, 0) # TODO: Convert the color option to RGB

#               # Generate the text to insert
#               if options["text"] == "insert only page number (recommended)":
#                   text = str(i+1)
#               elif options["text"] == "page {n}":
#                   text = f"page {i+1}"
#               elif options["text"] == "page {n} of {x}":
#                   text = f"page {i+1} of {total_pages}"
#               else:
#                   text = options["text"].replace("{n}", str(i+1)).replace("{x}", str(total_pages)).replace("{total}", str(total_pages))

#               # TODO: Position the page number based on the bulletPosition option
#               overlay.cell(200, 10, txt=text, ln=True, align='C')

#               # Merge the overlay with the current page
#               page.merge_page(overlay)

#           # Add the page to the writer
#           writer.add_page(page)
#       output_path = os.path.join(tmpdirname, 'output.pdf')
#       with open(output_path, "wb") as f:
#           writer.write(f)

#       # Move the file to a permanent location
#       permanent_path = os.path.join('/tmp', 'output.pdf')
#       shutil.move(output_path, permanent_path)

#       return permanent_path


import os
import tempfile
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


"""
    When we choose the ‘Facing pages’ option,
    the pages are arranged in pairs, with the left and right pages forming a spread.
    This allows you to design your document with the understanding that the reader will see two pages at once.
    The position of the page numbers in a PDF file can change when the layout is set to ‘Facing pages’. In this layout,
    the page numbers are usually placed on the outside corners of the pages, rather than the inside corners as in the single page layout. This is because the inside corners of the pages are often obscured by the binding when the document is printed and bound1.

    we should position the nubmers as before if they coose "top center" or "bottom center" for the bulletPosition.
    but when they choose one of the corners for the bulletPosition i.e "top left" | "top right" | "bottom left" | "bottom right"
    if they choose "top left" {
        each odd number page should be numbered on "top right" and each even number page should be numbered "top left"
        for example page 1 should be numbered "top right" and page 2 number should appear "top left".
    } same thing for "bottom left" but on the bottom side.

    if they choose "top right" {
        this is the opposite of "top left"
        i.e 
        each odd number page should be numbered on "top left" and each even number page should be numbered "top right"
        for example page 1 should be numbered "top left" and page 2 number should appear "top right".
    } same thing for "bottom right" but on the bottom side.
    this should happen with taking the value of firstPageIsCover (if true) into consideration.
    i.e if firstPageIsCover then the first page of the pdf should not be counted as the first page of the pdf file when numbering right?
"""
def number_pdf(file, options):
    # Step 1: Store the file as a temporary file
    print(options)
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, file.filename)
    file.save(temp_file)

    # Step 2: Add page numbers to each page
    output_pdf = PdfWriter()
    input_pdf = PdfReader(temp_file)

    start_page = options.get('startPage', 0)
    range_to_number = options.get('rangeToNumber', {'start': 0, 'end': len(input_pdf.pages)})
    text = options.get('text', 'insert only page number (recommended)')
    first_page_is_cover = options.get('firstPageIsCover', False)

    # Define margin and font size
    margin_map = {'small': 10, 'recommended': 20, 'big': 30}
    margin = margin_map.get(options.get('margin', 'recommended'))
    font_size = options.get('fontSize', 12)
    is_bold = options.get('isBold', False)
    is_italic = options.get('isItalic', False)
    is_underlined = options.get('isUnderlined', False)
    color = options.get('color', '#000000')
    font = options.get('font', 'Helvetica')

    # Convert hex color to RGB
    color = Color(*[int(color[i:i+2], 16)/255 for i in (1, 3, 5, 7)])

    # Map font names
    font_map = {
        'arial': 'Helvetica',
        'courier-new': 'Courier',
        'helvetica': 'Helvetica',
        'times-new-roman': 'Times-Roman'
    }
    font = font_map.get(font.lower(), 'Helvetica')

    # Set font style
    if is_bold and is_italic:
        font += "-BoldOblique"
    elif is_bold:
        font += "-Bold"
    elif is_italic:
        font += "-Oblique"

    for i, page in enumerate(input_pdf.pages):
        if range_to_number['start'] <= i <= range_to_number['end'] and not (first_page_is_cover and i == 0):
            fd, path = tempfile.mkstemp()
            packet = open(path, 'wb')

            # Create a new PDF canvas with the page number
            can = canvas.Canvas(packet)
            can.setFontSize(font_size)
            can.setFillColor(color)
            can.setFont(font, font_size)

            # Determine the position of the page number
            bulletPosition = options.get('bulletPosition', 'bottom center').split()
            y = margin if bulletPosition[0] == 'bottom' else page.mediabox[3] - margin
            x = margin if bulletPosition[1] == 'left' else page.mediabox[2] - margin if bulletPosition[1] == 'right' else page.mediabox[2] / 2

            page_number = i + start_page
            if text == 'insert only page number (recommended)':
                can.drawString(x, y, f'{page_number}')
            elif text == 'page {n}':
                can.drawString(x, y, f'page {page_number}')
            elif text == 'page {n} of {x}':
                can.drawString(x, y, f'page {page_number} of {len(input_pdf.pages)}')
            else:
                custom_text = text.replace('{n}', str(page_number)).replace('{x}', str(len(input_pdf.pages)))
                can.drawString(x, y, custom_text)

            # Draw underline if needed
            if is_underlined:
                can.line(x, y, x + can.stringWidth(page_number, font, font_size), y)

            can.save()

            # Close the packet file
            packet.close()

            # Merge the page number canvas with the original page
            watermark = PdfReader(path)
            page.merge_page(watermark.pages[0])

            # Delete the temporary file
            os.close(fd)
            os.remove(path)

        # Add the page (modified or not) to the output PDF
        output_pdf.add_page(page)

    # Step 3: Save the modified PDF with page numbers
    output_file = os.path.join(temp_dir, 'numbered_pdf.pdf')
    with open(output_file, 'wb') as f:
        output_pdf.write(f)

    # Step 4: Return the path to the modified PDF
    return output_file
