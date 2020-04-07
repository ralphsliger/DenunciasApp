#controlador dashboard

from flask import Blueprint 

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
def index():
    return "hello from dashboard"
    
    

