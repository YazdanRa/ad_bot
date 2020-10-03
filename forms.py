from flask_wtf  import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flask_login import current_user
from flask_wtf.file import FileAllowed,FileField
import os 
import secrets


class LoginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=4,max=8) ])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8)])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')