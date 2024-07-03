from flask_smorest import abort

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def is_file_allowed(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.lower() in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


def allowed_file_or_abort(file, slug, type):
    if file is None or not is_file_allowed(file.filename):
        abort(400, message=f"{type} is required and must be a {' or '.join(ALLOWED_EXTENSIONS)} file")
    else:
        filename = f"ggy-{slug}-{type}.{file.filename.rsplit('.', 1)[1].lower()}"
        file_data = {
            "file": file,
            "filename": filename,
            "type": type,
        }

        return file_data
