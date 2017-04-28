from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField, TextAreaField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegisterForm(FlaskForm):
    firstname = StringField('firstname', validators=[InputRequired()])
    lastname = StringField('lastname', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    
class WishForm(FlaskForm):
    url = StringField('Web Address', validators=[InputRequired()])
    thumbnail = TextField('Image')
    title = TextField('Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    