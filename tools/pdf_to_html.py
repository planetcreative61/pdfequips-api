"""
    the pdf_to_html below is working fine and just like i wanted.
    now please also give me the implementation of this pdf_to_html_multiple(files) function, which does the same thing as the pdf_to_html but it converts multiple pdf files and returns a zip folder containing all of the result.
    keep in mind that this function should preserve the original file names. for example if the passed flask file object list is a list of two files a.pdf and b.pdf the resulting zip folder should contain two files a.html and b.html.
    meaning that the resulting files should be named the same name as the original filenames without the extension part which is .pdf.
"""

import os
import tempfile
import subprocess
import glob
import shutil
import zipfile

def pdf_to_html(file):
 # Create a temporary PDF file
 temp_pdf = tempfile.NamedTemporaryFile(delete=False)

 # Save the incoming file to the temporary file
 file.save(temp_pdf.name)

 # Convert the PDF to HTML using pdf2htmlEX
 subprocess.run(["pdf2htmlEX", temp_pdf.name, "--dest-dir", os.path.dirname(temp_pdf.name)], check=True)

 # Get the latest HTML file in the temporary directory
 temp_dir = os.path.dirname(temp_pdf.name)
 list_of_files = glob.glob(temp_dir + '/*.html')
 latest_file = max(list_of_files, key=os.path.getctime)

 # Close and delete the temporary PDF file
 temp_pdf.close()

 return latest_file



# this function is not working!
def pdf_to_html_multiple(files):
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    # Convert each PDF file to HTML
    html_files = []
    for file in files:
        # Create a temporary PDF file
        temp_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)

        # Save the incoming file to the temporary PDF file
        file.save(temp_pdf.name)

        # Convert the PDF to HTML using pdf2htmlEX
        subprocess.run(["pdf2htmlEX", temp_pdf.name, "--dest-dir", temp_dir], check=True)

        # Get the latest HTML file in the temporary directory
        list_of_files = glob.glob(os.path.join(temp_dir, '*.html'))
        latest_file = max(list_of_files, key=os.path.getctime)
        html_files.append(latest_file)

        # Close and delete the temporary PDF file
        temp_pdf.close()
        os.remove(temp_pdf.name)

    # Create a zip folder containing all the HTML files
    zip_filename = os.path.join(temp_dir, 'html_files.zip')
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for html_file in html_files:
            filename = os.path.splitext(os.path.basename(html_file))[0] + '.html'
            zip_file.write(html_file, arcname=filename)

    # Remove the temporary directory
    shutil.rmtree(temp_dir)

    return zip_filename