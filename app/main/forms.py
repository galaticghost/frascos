from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length
from app import db
from app.utils import file_is_allowed
        
class PostForm(FlaskForm):
    post = TextAreaField(validators=[DataRequired(), Length(min=1, max=150)])
    submit = SubmitField("Post")
            
class EditUsernameForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    submit = SubmitField("Edit")

    def __init__(self,username,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.current_username = username

    def validate_username(self,username):
        if username.data == self.current_username:
            raise ValidationError("Your username must be different")
        else:
            user = db.cur.execute("SELECT 1 FROM users WHERE username = %s;",(username.data,)).fetchone()
            if user is not None:
                raise ValidationError("This username is already taken")
            
class EditAboutMeForm(FlaskForm):
    about_me = TextAreaField("About me",validators=[Length(max=150)])
    submit = SubmitField("Edit")

    def __init__(self,about_me,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.current_about_me = about_me

    def validate_about_me(self,about_me):
        if self.current_about_me == about_me.data:
            raise ValidationError()

class EditProfilePictureForm(FlaskForm):
    profile_picture = FileField("Profile Picture",validators=[DataRequired()])
    submit = SubmitField("Edit")

    def validate_profile_picture(self,profile_picture):
        if file_is_allowed(profile_picture.data.filename) == False:
            raise ValidationError()
            
class EmptyForm(FlaskForm):
    submit = SubmitField("Submit")