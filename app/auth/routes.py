from app.auth import bp
from app.auth.forms import LoginForm,RegistrationForm
from app import db
from app.models import User
from flask import render_template,redirect,flash,url_for,request
from werkzeug.security import generate_password_hash
from flask_login import current_user,login_user,logout_user

@bp.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        result = db.cur.execute("SELECT id,username,email,password,profile_picture,last_seen,about_me FROM users WHERE username = %s ;",
                            (form.username.data,)).fetchone()
        user = User(id=result["id"],username=result["username"],email=result["email"],password_hash=result["password"],
                profile_picture=result["profile_picture"],last_seen=result["last_seen"],about_me=result.get("about_me")) if result is not None else None
        if user is None or not user.check_password(form.password.data):
            flash("Wrong username or password")
            return redirect(url_for("auth.login"))
        
        login_user(user,remember=form.remember_me.data)
        
        next_page = request.args.get("next","main.index")
        return redirect(next_page)
        
    return render_template("auth/login.jinja",title="Sign In", form=form)

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@bp.route("/register", methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        db.cur.execute("INSERT INTO users(email,username,password) VALUES (%s,%s,%s);",
                       (form.email.data,form.username.data,password_hash))
        db.conn.commit()
        return redirect(url_for("auth.login"))
    return render_template("auth/register.jinja", title="Sign Up", form=form)
