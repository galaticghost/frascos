from flask import Flask
from app.db import Database
from flask_login import LoginManager
from config import Config

login = LoginManager()
login.login_view = "auth.login"
db = Database()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url="/auth")

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app