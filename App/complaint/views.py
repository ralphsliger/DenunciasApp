### Controlador Modulo Complaint

from flask import Blueprint, render_template, request, session, redirect, url_for, abort 
import bson
from complaint.forms import BasicComplaintForm, EditComplaintForm
from user.decorators import login_required
from complaint.models import Complaint
from user.models import User
from utilities.storage import upload_image_file 



complaint_page = Blueprint('complaint_page', __name__)

@complaint_page.route('/create', methods=['GET','POST'])
@login_required
def create():
    form = BasicComplaintForm()
    error = None
    if request.method == 'POST' and form.validate():
        error= form.errors
        print(error)
        if not error:
            user = User.objects.filter(email=session.get('email')).first()
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


@complaint_page.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    try:
        complaint = Complaint.objects.filter(id=bson.ObjectId(id)).first()
    except bson.errors.InvalidId:
        abort(404)     
    user = User.objects.filter(email=session.get('email')).first()
    if complaint and complaint.complainer == user.id:
        error = None
        message = None
        form = EditComplaintForm(obj=complaint)
        if request.method == 'POST' and form.validate():
            error= form.errors
            print(error)
            if not error:
                form.populate_obj(complaint)
                if form.lng.data and form.lat.data:
                    complaint.location = [form.lng.data, form.lat.data]
                image_url = upload_image_file(request.files.get('complaint'), 'complaint_photo', str(complaint.id))
                if image_url:
                    complaint.complaint_photo = image_url
                complaint.save()
                message = 'Complaint updated'
        return render_template('complaint/edit.html', form=form, error=error,
                              message=message, complaint=complaint)
    else:
        abort(404)
