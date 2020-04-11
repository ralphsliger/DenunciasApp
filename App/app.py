#inicializador general de todos los componentes
from flask import Flask
from flask_mongoengine import MongoEngine 
import sys

db = MongoEngine()

def created_app(config=None):
    
    app = Flask(__name__)
    
    if config is not None:
        app.config.from_object(config)
    
    db.init_app(app)
    from user.views import user_page
    app.register_blueprint(user_page, url_prefix='/user')

    return app 

