from wtforms import Form, StringField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from user.models import User

class RegistrationForm(Form):
    username = StringField('Your Username', [validators.DataRequired(),validators.Length(min=2,max=30)])
    name = StringField('Your Name', [validators.DataRequired(),validators.Length(min=2,max=30)])
    lastname = StringField('Your Name', [validators.DataRequired(),validators.Length(min=2,max=30)])
    city = StringField('Your City', [validators.DataRequired(),validators.Length(min=2,max=30)])
    email = EmailField('Email Adress', [validators.DataRequired(), validators.Email()])
    password = PasswordField('New password', [validators.DataRequired(), validators.EqualTo('confirm', message='password must match')])
    confirm = PasswordField('Repeat password')
