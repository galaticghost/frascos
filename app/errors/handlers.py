from app import db
from app.errors import bp
from flask import render_template

@bp.app_errorhandler(404)
def not_found(e):
    return render_template("errors/404.jinja")

@bp.app_errorhandler(413)
def maximum_size(e):
    return render_template("errors/413.jinja")

@bp.app_errorhandler(500)
def internal_error(e):
    db.conn.rollback()
    return render_template("errors/500.jinja")