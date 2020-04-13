#controlador de modulo user
from flask import Blueprint, render_template, request
from user.models import User
from user.forms import RegistrationForm


user_page = Blueprint('user_page', __name__)

@user_page.route('/login')
def login():
    #user = User(username='ralphsliger',name='ralph',lastname='sliger',city='cartagena',email='r@r.com',password='123')
    #user.save()
    #return 'Hello {}!, {} {} from {} with {}!'.format(user.username, user.name, user.lastname, user.city, user.email)
    return render_template('base.html')

@user_page.route('/signup',methods=['GET', 'POST'])
def signup():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        return 'formulario'
    return render_template('user/signup.html', form=form)

