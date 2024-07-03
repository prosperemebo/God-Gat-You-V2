from flask_smorest import abort

ALLOWED_EXTENSIONS = {"PNG", "JPG", "JPEG"}


def is_file_allowed(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


def allowed_file_or_abort(file, message, slug, type):
    if not is_file_allowed(file.filename):
        abort(400, message=message)
    else:
        filename = f"ggy-{slug}-{type}.{file.filename.rsplit('.', 1)[1].lower()}"
        file_data = {
            "file": file,
            "filename": filename,
            "type": type,
        }

        return file_data
