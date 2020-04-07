#inicilizador app general 
from flask import Flask

app = Flask(__name__)

app.config.from_object('configuration.DevelopmentConfig')

#instancia controladores 
from app.denuncia.denuncia import denuncia
from app.dashboard.dashboard import dashboard

app.register_blueprint(denuncia)
app.register_blueprint(dashboard)
