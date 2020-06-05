### Controlador Modulo Complaint

from flask import Blueprint, render_template, request, session, redirect, url_for, abort 
from complaint.forms import BasicComplaintForm
from user.decorators import login_required
from complaint.models import Complaint
from user.models import User



complaint_page = Blueprint('complaint_page', __name__)

@complaint_page.route('/create', methods=['GET','POST'])
@login_required
def create():
    form = BasicComplaintForm()
    error = None
    if request.method == 'POST' and form.validate():
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
    
    return render_template('complaint/create.html', form=form)

