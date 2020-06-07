### Controlador Modulo Complaint

from flask import Blueprint, render_template, request, session, redirect, url_for, abort 
import bson
from complaint.forms import BasicComplaintForm, EditComplaintForm, CancelComplaintForm
from user.decorators import login_required
from complaint.models import Complaint
from user.models import User
from utilities.storage import upload_image_file



complaint_page = Blueprint('complaint_page', __name__)

#Crear queja
@complaint_page.route('/create', methods=['GET','POST'])
@login_required
def create():
    #instancia formulario 
    form = BasicComplaintForm()
    error = None
    #validar formulario y post request
    if request.method == 'POST' and form.validate():
        error= form.errors
        print(error)
        if not error:
            #si el usuario tiene sesion activa
            user = User.objects.filter(email=session.get('email')).first()
           #almacenar en bd
            complaint= Complaint(
                name=form.name.data,
                place=form.place.data,
                location=[form.lng.data, form.lat.data],
                description = form.description.data,
                complainer= user.id,
                follow= [user]
            )
            complaint.save()
            return redirect(url_for('complaint_page.edit', id=complaint.id))
    return render_template('complaint/create.html', form=form)

#editar queja
@complaint_page.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    try:
        #filtar id denuncia
        complaint = Complaint.objects.filter(id=bson.ObjectId(id)).first()
    except bson.errors.InvalidId:
        abort(404)     
        #si el usuario tiene sesion activa
    user = User.objects.filter(email=session.get('email')).first()
    if complaint and complaint.complainer == user.id:
        error = None
        message = None
        #instanciar formulario
        form = EditComplaintForm(obj=complaint)
        if request.method == 'POST' and form.validate():
            if not error:
                form.populate_obj(complaint)
                #tomar valores de latitud y longitud y guardarlos en un array 'location'
                if form.lng.data and form.lat.data:
                    complaint.location = [form.lng.data, form.lat.data]
                # guardar imagen denuncia 
                image_url = upload_image_file(request.files.get('photo'), 'complaint_photo', str(complaint.id))
                if image_url:
                    complaint.complaint_photo = image_url
                complaint.save()
                message = 'Complaint updated'
        return render_template('complaint/edit.html', form=form, error=error,
                              message=message, complaint=complaint)
    else:
        abort(404)

#cancelar queja
@complaint_page.route('/<id>/cancel', methods=['GET','POST'])
@login_required
def cancel(id):
    try:
        #filtrar id queja
        complaint = Complaint.objects.filter(id=bson.ObjectId(id)).first()
    except bson.errors.InvalidId:
        abort(404)
        #verificar sesion usuario
    user = User.objects.filter(email=session.get('email')).first()
    
    #si el denunciante y la queja tienen el mismo userid y /cancel desactivado
    if complaint and complaint.complainer == user.id and complaint.cancel == False:
        error = None
        form = CancelComplaintForm()
        if request.method == 'POST' and form.validate():
            #escribir yes para confirmar cancelacion
            if form.confirm.data == 'yes':
                complaint.cancel = True
                complaint.save()
                return redirect(url_for('complaint_page.edit', id=complaint.id))
            else:
                error = 'Say yes if you want to cancel'
        return render_template('complaint/cancel.html', form=form, error=error, complaint=complaint)
    else:
        abort(404)

#Mostrar Queja
@complaint_page.route('/<id>', methods=['GET'])
def public(id):
    try:
        #filtrar id queja
        complaint = Complaint.objects.filter(id=bson.ObjectId(id)).first()
    except bson.errors.InvalidId:
        abort(404)
        
        
    if complaint:
        complainer = User.objects.filter(id=complaint.complainer).first()
        user = User.objects.filter(email=session.get('email')).first()
        return render_template('complaint/public.html', complaint=complaint, complainer=complainer, user=user)
    else:
        abort(404)

#Apoyar denuncia
@complaint_page.route('/<id>/support', methods=['GET'])
@login_required
def support(id):
    user = User.objects.filter(email=session.get('email')).first()
    try:
        complaint = Complaint.objects.filter(id=bson.ObjectId(id)).first()
    except bson.errors.InvalidId:
        abort(404)    
    
    if user and complaint:
        if user not in complaint.follow:
            complaint.follow.append(user)
            complaint.save()
        return redirect(url_for('complaint_page.public', id=id))
    else:
        abort(404)

#dejar de apoyar las denuncias   
@complaint_page.route('/<id>/unsupport', methods=['GET'])
@login_required
def unsupport(id):
    user = User.objects.filter(email=session.get('email')).first()
    try:
        complaint = Complaint.objects.filter(id=bson.ObjectId(id)).first()
    except bson.errors.InvalidId:
        abort(404)   
    
    if user and complaint:
        if user in complaint.follow:
            complaint.follow.remove(user)
            complaint.save()
        return redirect(url_for('complaint_page.public', id=id))
    else:
        abort(404)

#listado de denuncias hechas (como usuario registrado)
@complaint_page.route('/manage/<int:complaint_page_number>', methods=['GET'])
@complaint_page.route('/manage', methods=['GET'])
@login_required
def manage(complaints_page_number=1):
    user = User.objects.filter(email=session.get('email')).first()
    if user:
        complaints = Complaint.objects.filter(complainer=user.id).order_by('name').paginate(page=complaints_page_number, per_page=4)
        return render_template('complaint/manage.html', complaints=complaints)
    else:
        abort(404)     

#Listado global de denuncias
@complaint_page.route('/explore/<int:complaint_page_number>', methods=['GET'])
@complaint_page.route('/explore', methods=['GET'])
def explore(complaint_page_number=1):
    place = request.args.get('place')
    try:
        lng = float(request.args.get('lng'))
        lat = float(request.args.get('lat'))
        complaints = Complaint.objects(location__near=[lng, lat], location__max_distance=100000,
                               cancel=False).paginate(page=complaint_page_number, per_page=4)
        return render_template('complaint/explore.html', complaints=complaints, place=place, lng=lng, lat=lat)
    except:
        return render_template('complaint/explore.html', place=place)



