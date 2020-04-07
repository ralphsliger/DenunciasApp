#controlador modulo denuncia

from flask import Blueprint 

denuncia = Blueprint('denuncia', __name__)

@denuncia.route('/denuncia')
def index():
    return "hello from denuncia"
    

