import tempfile
import os
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF
import subprocess
import re

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
