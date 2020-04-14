#controlador de modulo user
from flask import Blueprint, render_template, request, session, redirect, url_for
from user.models import User
from user.forms import RegistrationForm
from user.forms import LoginForm
import bcrypt
from user.decorators import login_required


user_page = Blueprint('user_page', __name__)

@user_page.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        user = User.objects.filter(email=form.email.data).first()
        if user:
            if bcrypt.checkpw(form.password.data, user.password):
                session['email'] = user.email
                return redirect(request.args.get('next') or url_for('hello'))
            else:
                user = None
        if not user:
            error = 'Your email or password was entered incorrectly'
    return render_template('user/login.html', form=form, error=error)


@user_page.route('/logout')
def logout():
    session.pop('email')
    return redirect(url_for('user_page.login'))



@user_page.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)   
        user = User(      
            username= form.username.data,
            name= form.name.data,
            lastname= form.lastname.data,
            city= form.city.data,
            email= form.email.data,
            password= hashed_password
        )
        user.save()
        return 'registrado con exito'
    return render_template('user/signup.html', form=form)

@user_page.route('/edit', methods=['POST','GET'])
@login_required
def edit():
    user = User.objects.filter(email=session['email']).first()
    return render_template('user/edit.html', user=user)