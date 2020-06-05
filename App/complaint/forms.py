from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, validators, ValidationError,  FloatField
from wtforms.fields.html5 import EmailField
from user.models import User
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileAllowed

class BasicComplaintForm(Form):
    name = StringField('Nombre Denuncia', validators=[validators.DataRequired(), validators.Length(min=2, max=80)])
    gplace = StringField('Google Place Api')
    place = StringField('Place', validators=[validators.DataRequired()], widget= TextArea())
    lng = FloatField('Longitude', validators=[validators.Optional()])
    lat = FloatField('Latitude', validators=[validators.Optional()])
    description = StringField('Descripcion' , validators=[validators.DataRequired()])


