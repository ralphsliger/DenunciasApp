from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, ValidationError,  FloatField
from user.models import User
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileAllowed

class BasicComplaintForm(FlaskForm):
    name = StringField('Nombre Denuncia', validators=[validators.DataRequired()])
    gplace = StringField('Google Place Api')
    place = StringField('Place', widget= TextArea())
    lng = FloatField('Longitude', validators=[validators.Optional()])
    lat = FloatField('Latitude', validators=[validators.Optional()])
    description = StringField('Descripcion' , validators=[validators.DataRequired()])

class EditComplaintForm(BasicComplaintForm):
    photo = FileField('Complaint Photo', [FileAllowed(['jpg','jpeg','png'], 'Only allowed .jpg .png files')])