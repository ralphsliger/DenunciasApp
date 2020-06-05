### Controlador Modulo Complaint

from flask import Blueprint, render_template, request, session, redirect, url_for, abort 
from complaint.forms import BasicComplaintForm
from user.decorators import login_required

complaint_page = Blueprint('complaint_page', __name__)

@complaint_page.route('/create', methods=['GET','POST'])
@login_required
def create():
    form = BasicComplaintForm()
    return render_template('complaint/create.html', form=form)

