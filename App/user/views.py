#controlador de modulo user
from flask import Blueprint
from user.models import User

user_page = Blueprint('user_page', __name__)

@user_page.route('/login')
def login():
    user = User(username='ralphsliger',name='ralph',lastname='sliger',city='cartagena',email='r@r.com',password='123')
    user.save()
    return 'Hello {}!, {} {} from {} with {}!'.format(user.username, user.name, user.lastname, user.city, user.email)


