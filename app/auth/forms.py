from app import db
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign in")

class RegistrationForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    password2 = PasswordField("Password",validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self,username):
        user = db.cur.execute("SELECT 1 FROM users WHERE username = %s;",(username.data,)).fetchone()
        if user is not None:
            raise ValidationError("Please use a different username")
        
    def validate_email(self,email):
        email = db.cur.execute("SELECT 1 FROM users WHERE email = %s;",(email.data,)).fetchone()
        if email is not None:
            raise ValidationError("Please use a different email")