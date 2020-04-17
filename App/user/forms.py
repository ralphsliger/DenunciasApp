from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, validators, ValidationError
from wtforms.fields.html5 import EmailField
from user.models import User

class RegistrationForm(Form):
    username = StringField('Your Username', [validators.DataRequired(),validators.Length(min=2,max=30)])
    name = StringField('Your Name', [validators.DataRequired(),validators.Length(min=2,max=30)])
    lastname = StringField('Your Last Name', [validators.DataRequired(),validators.Length(min=2,max=30)])
    city = StringField('Your City', [validators.DataRequired(),validators.Length(min=2,max=30)])
    email = EmailField('Email Adress', [validators.DataRequired(), validators.Email()])
    password = PasswordField('New password', [validators.DataRequired(), validators.EqualTo('confirm', message='password must match')])
    confirm = PasswordField('Repeat password')

    def validate_email(FlaskForm, field):
        if User.objects.filter(email=field.data.lower()).first():
            raise ValidationError('Email address alreay in use')


class LoginForm(Form):
    email= EmailField('Email address', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])
