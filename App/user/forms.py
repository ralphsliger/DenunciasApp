from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, validators, ValidationError
from wtforms.fields.html5 import EmailField
from user.models import User
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileAllowed

class BaseUserForm(Form):
    name = StringField('Your Name', [validators.DataRequired(),validators.Length(min=2,max=30)])
    lastname = StringField('Your Last Name', [validators.DataRequired(),validators.Length(min=2,max=30)])
    city = StringField('Your City', [validators.DataRequired(),validators.Length(min=2,max=30)])
    email = EmailField('Email Adress', [validators.DataRequired(), validators.Email()])

class RegistrationForm(BaseUserForm): 
    password = PasswordField('New password', [
        validators.DataRequired(), 
        validators.EqualTo('confirm', message='password must match')])
    confirm = PasswordField('Repeat password')

    def validate_email(Form, field):
        if User.objects.filter(email=field.data.lower()).first():
            raise ValidationError('Email address alreay in use')

class EditProfileForm(BaseUserForm):
    bio = StringField('Bio', widget=TextArea(), validators=[validators.Length(max=200)])
    image = FileField('Profile image', [FileAllowed(['jpg','jpeg','png'], 'Only allowed .jpg .png files')])

class LoginForm(Form):
    email= EmailField('Email address', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])

class PasswordForm(Form):
    old_password = PasswordField('Old Password', [validators.DataRequired()])
    new_password = PasswordField('New Password', [validators.DataRequired(),
                                                 validators.EqualTo('confirm',
                                                                    message='Passwords must match')])
    confirm = PasswordField('Confirm Password')