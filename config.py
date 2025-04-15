import os

class Config:
    SECRET_KEY = os.urandom(10).hex()
    MAX_CONTENT_LENGTH = 25 * 1000 * 1000
ALLOWED_FILES = {"png","jpg","gif","jpeg"}
ALLOWED_IMAGES = {"png","jpg","gif","jpeg"}
IMAGES_PATH = 'app/static/profile_pictures/'
