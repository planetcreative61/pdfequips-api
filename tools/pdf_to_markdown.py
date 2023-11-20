"""
    the pdf_to_markdown function is converting a single pdf file into a markdown file
    i want another similar function but to convert multiple pdf files to md files using the same approach.
    but with a slightly little changes like:
    1 - this function should return a zip folder containing all the converted md files instead of a single md file.
    2 - all the md files inside the returned zip folder should be named the same names as the original files.
    for example if the passed flask file object list is a list of two pdf files: a.pdf and b.pdf
    then the funciton is expected to return a zip folder containing two files a.md and b.md i.e the files in the zip folder should be named same name as the original filenames except the extension of the original files which is .pdf
"""
import tempfile
import os
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF
import subprocess
import re
import zipfile

def cleanup_markdown(pandoc_markdown):
    # Remove custom style attributes
    cleaned_markdown = re.sub(r'{style=".*?"}', '', pandoc_markdown)

    # Reformat headers (This might need further refinement based on your specific headers)
    cleaned_markdown = re.sub(r'\*\*\[(.*?)\]', r'# \1', cleaned_markdown)

    # Adjust links (This might need further refinement based on your specific links)
    cleaned_markdown = re.sub(r'\[([^]]*)]\(([^)]*)\)', r'[\1](\2)', cleaned_markdown)

    # Additional cleanups for styling indicators, lists, etc.

    return cleaned_markdown

def pdf_to_markdown(file):
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    # Get a secure filename and create the temporary file path
    temp_file_path = os.path.join(temp_dir, secure_filename(file.filename))

    # Save the incoming file to the temporary file
    file.save(temp_file_path)

    # Open the PDF file using PyMuPDF
    pdf_document = fitz.open(temp_file_path)

    # Initialize variables to store the HTML content
    html_content = ''

    # Iterate through each page in the PDF
    for page in pdf_document:
        # Generate HTML per page
        html_content += page.get_text("html")

    # Create an HTML file and write the content into it
    html_file_path = os.path.join(temp_dir, 'converted.html')
    with open(html_file_path, 'w') as html_file:
        html_file.write(html_content)

    # Convert HTML to Markdown using pandoc
    markdown_file_path = os.path.join(temp_dir, 'converted.md')
    pandoc_command = f"pandoc {html_file_path} -f html -t markdown -o {markdown_file_path}"
    subprocess.run(pandoc_command, shell=True)

    # Read the generated Markdown file
    with open(markdown_file_path, 'r') as md_file:
        markdown_content = md_file.read()

    # Clean up the Markdown content
    cleaned_markdown = cleanup_markdown(markdown_content)

    # Write cleaned Markdown content back to the file
    cleaned_markdown_file_path = os.path.join(temp_dir, 'cleaned.md')
    with open(cleaned_markdown_file_path, 'w') as cleaned_md_file:
        cleaned_md_file.write(cleaned_markdown)

    # Return the path of the cleaned Markdown file
    return cleaned_markdown_file_path




# def convert_pdf_to_markdown(pdf_file):
#     temp_dir = tempfile.mkdtemp()
#     temp_file_path = os.path.join(temp_dir, secure_filename(pdf_file.filename))
#     pdf_file.save(temp_file_path)
#     pdf_document = fitz.open(temp_file_path)

#     html_content = ''
#     for page in pdf_document:
#         html_content += page.get_text("html")

#     html_file_path = os.path.join(temp_dir, 'converted.html')
#     with open(html_file_path, 'w') as html_file:
#         html_file.write(html_content)

#     markdown_file_path = os.path.join(temp_dir, 'converted.md')
#     pandoc_command = f"pandoc {html_file_path} -f html -t markdown -o {markdown_file_path}"
#     subprocess.run(pandoc_command, shell=True)

#     with open(markdown_file_path, 'r') as md_file:
#         markdown_content = md_file.read()

#     cleaned_markdown = cleanup_markdown(markdown_content)

#     cleaned_markdown_file_path = os.path.join(temp_dir, 'cleaned.md')
#     with open(cleaned_markdown_file_path, 'w') as cleaned_md_file:
#         cleaned_md_file.write(cleaned_markdown)

#     return cleaned_markdown_file_path

def pdf_to_markdown_multiple(pdf_files):
    temp_dir = tempfile.mkdtemp()
    zip_file_path = os.path.join(temp_dir, 'converted_files.zip')

    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for pdf_file in pdf_files:
            md_file_path = pdf_to_markdown(pdf_file)
            base_name = os.path.splitext(pdf_file.filename)[0] + '.md'
            zipf.write(md_file_path, arcname=base_name)

    return zip_file_path, temp_dir