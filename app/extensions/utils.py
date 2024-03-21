import base64
import uuid


def save_base64_file(data):
    file_name = str(uuid.uuid4())
    banner_img_location = "./static/" + file_name
    with open(banner_img_location, "wb") as fh:
        base64_str = data
        base64_str = base64_str.split(
            ',')[1] if ',' in base64_str else base64_str

        missing_padding = len(base64_str) % 4
        if missing_padding != 0:
            base64_str += '=' * (4 - missing_padding)
        fh.write(base64.decodebytes(
            base64_str.encode('utf-8')))
    return file_name
