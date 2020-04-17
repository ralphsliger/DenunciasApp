#controlador de modulo user
from flask import Blueprint, render_template, request, session, redirect, url_for, abort
from user.models import User
from user.forms import RegistrationForm, LoginForm, EditProfileForm
import bcrypt
from user.decorators import login_required


user_page = Blueprint('user_page', __name__)

@user_page.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None
        # si request es post y el formato ha sido validado compara el hash en la base de datos
    if request.method == 'POST' and form.validate():
        user = User.objects.filter(email=form.email.data.lower()).first()
        if user:
            if bcrypt.checkpw(form.password.data, user.password):
                session['email'] = user.email
                #return redirect(request.args.get('next') or url_for('home'))
                return 'logeado'
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
    #instancia formulario de registro
    form = RegistrationForm(request.form)
    # si request es post y el formato ha sido validado registra el usuario
    if request.method == 'POST' and form.validate():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)   
        user = User(      
            name= form.name.data,
            lastname= form.lastname.data,
            city= form.city.data,
            email= form.email.data.lower(),
            password= hashed_password
        )
        user.save()
        return 'registrado con exito'
    return render_template('user/signup.html', form=form)

@user_page.route('/edit', methods=['POST','GET'])
@login_required
def edit():
    user = User.objects.filter(email=session['email']).first()
    if user: 
        error = None
        message = None
        form = EditProfileForm(obj=user)

        if request.method == 'POST' and form.validate():
            if user.email != form.email.data.lower():
                if User.objects.filter(email=form.email.data.lower()).first():
                    error = 'Email is already in use'
                else: 
                    session['email'] = form.email.data.lower()
            if not error:
                form.populate_obj(user)
                user.save()
                message = 'Profile updated'

        return render_template('user/edit.html', user=user, form=form, error=error, message=message)
    else:
        abort(404)