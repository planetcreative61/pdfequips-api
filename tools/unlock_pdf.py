import zipfile
import uuid
import pikepdf
import tempfile
from io import BytesIO

# even after providing the correct password it rises the invalid password error


def unlock_pdf_file(file, password):
    # Save the file to a temporary location
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp_file.name)
    temp_file.close()

    try:
        pdf = pikepdf.open(temp_file.name, password=password,
                           allow_overwriting_input=True)
    except pikepdf._core.PasswordError:
        raise ValueError("Invalid password provided")

    if not pdf.is_encrypted:
        with open(temp_file.name, 'rb') as file:
            return file.read()

    pdf.save(temp_file.name)

    # Read the saved file into a BytesIO object
    with open(temp_file.name, 'rb') as file:
        unlocked_pdf = BytesIO(file.read())

    pdf.close()

    # Read the content of the unlocked_pdf BytesIO object
    unlocked_file_content = unlocked_pdf.read()

    return unlocked_file_content


def unlock_multiple_pdf_files(files, passwords):
    zip_filename = f"/tmp/{uuid.uuid4()}.zip"

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for i, file in enumerate(files):
            # Get the ith password from the passwords list
            password = passwords[i % len(passwords)]
            unlocked_pdf = unlock_pdf_file(file, password)
            unlocked_filename = f"{file.filename.split('.')[0]}_unlocked.pdf"
            zip_file.writestr(unlocked_filename, unlocked_pdf)

    return zip_filename
