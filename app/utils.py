from flask import request
from config import ALLOWED_FILES,IMAGES_PATH
from secrets import token_hex
import os

def get_page():
    page = request.args.get("page", 1, type=int)
    if page < 1:
        page = 1
    offset = 30 * (page - 1)
    return offset,page

def file_is_allowed(filename):
    return "." in filename and \
        filename.rsplit(".",1)[1].lower() in ALLOWED_FILES

def generate_filename(name):
    hex_str = token_hex(16)
    _ ,file_extension = os.path.splitext(name)
    filename = hex_str + file_extension
    return filename

def delete_file(filename):
    if os.path.exists(os.path.join(IMAGES_PATH,filename)) \
        and (filename != "7b2666b68102643c39a0c4c2d095515e.png" or \
            filename != "d3badb0b2c80449763ef7610bd10915c.jpeg"):
        os.remove(os.path.join(IMAGES_PATH,filename))