import os
import tempfile
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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
    layout = options.get('layout', 'Single page')

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
    end_page = range_to_number['end'] if range_to_number['end'] is not None else len(input_pdf.pages)

    for i, page in enumerate(input_pdf.pages):
        if range_to_number['start'] <= i <= end_page and not (first_page_is_cover and i == 0):
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
            if layout == 'Facing pages' and bulletPosition[1] in ['left', 'right']:
                if (i + 1) % 2 == 0:  # even page
                    x = margin if bulletPosition[1] == 'right' else page.mediabox[2] - margin
                else:  # odd page
                    x = margin if bulletPosition[1] == 'left' else page.mediabox[2] - margin
            else:
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
