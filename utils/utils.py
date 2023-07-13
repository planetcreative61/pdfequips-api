from werkzeug.datastructures import FileStorage
import mimetypes
"""
    i want another function similar to this called is_jpg which checks if the file is jpg or not
    using the same approach
"""
def is_pdf(file):
    mime_type, _ = mimetypes.guess_type(file.filename)
    file.seek(0)  # Reset file pointer to the beginning
    return mime_type == 'application/pdf'


def is_jpg(file):
    mime_type, _ = mimetypes.guess_type(file.filename)
    file.seek(0)  # Reset file pointer to the beginning
    return mime_type == 'image/jpeg'


def is_valid_word(file) -> bool:
    if file is not None and (file.filename.endswith('.doc') or file.filename.endswith('.docx')):
        return True
    elif file is not None and (mimetypes.guess_type(file.filename) == 'application/msword' or mimetypes.guess_type(file.filename) == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
        return True
    else:
        return False



def is_xls(file):
    header = file.read(5)
    file.seek(0)
    return header == b'\xD0\xCF\x11\xE0\xA1'



def is_valid_excel(file) -> bool:
    if file is not None and (file.filename.endswith('.xls') or file.filename.endswith('.xlsx')):
        return True
    elif file is not None and (file.mimetype == 'application/vnd.ms-excel' or file.mimetype == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
        return True
    else:
        return False
def is_valid_powerpoint(file):
    if file.filename.endswith('.ppt') or file.filename.endswith('.pptx'):
        return True
    elif file.mimetype == 'application/vnd.ms-powerpoint' or file.mimetype == 'application/vnd.openxmlformats-officedocument.presentationml.presentation':
        return True
    else:
        return False



ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'doc',
                      'docx', 'xls', 'xlsx', 'ppt', 'pptx'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


def validate_file(files):
    max_files = 5
    if isinstance(files, FileStorage):
        files = [files]
    if len(files) > max_files:
        return "ERR_MAX_FILES_EXCEEDED"
    if len(files) <= 0:
        return "ERR_NO_FILES_SELECTED"
    for file in files:
        filename: str = file.filename  # type: ignore

        extension = filename.split('.')[-1]
        if not file:
            return 'FILE_CORRUPT'
        if not filename:
            return 'FILE_CORRUPT'
        if not file.content_type:
            return 'NOT_SUPPORTED_TYPE'
        file_contents = file.read()
        if len(file_contents) <= 0:
            return 'EMPTY_FILE'

        # Check file type
        if extension == 'pdf' and not is_pdf(file):
            return 'NOT_SUPPORTED_TYPE'
        elif extension == 'jpg' and not is_jpg(file):
            return 'NOT_SUPPORTED_TYPE'
        elif extension in ['doc', 'docx'] and not is_valid_word(file):
            return 'NOT_SUPPORTED_TYPE'
        elif extension in ['xls', 'xlsx'] and not is_valid_excel(file):
            return 'NOT_SUPPORTED_TYPE'
        elif extension in ['ppt', 'pptx'] and not is_valid_powerpoint(file):
            print("the error is here: is_valid_powerpoint(file):")
            return 'NOT_SUPPORTED_TYPE'

        if len(file_contents) > MAX_FILE_SIZE:
            return 'FILE_TOO_LARGE'

    return None