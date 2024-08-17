from flask import Flask
from .auth import auth
from .patient import patient
from .doctor import doctor
from .admin_g import admin_g
from .admin_d import admin_d
from .model import *
from .common_routes import common_route


app = Flask(__name__)

app.config['SECRET_KEY'] = "h27dh82cnjd129cnas"

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///database.db"

db.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(patient)
app.register_blueprint(admin_g)
app.register_blueprint(admin_d)
app.register_blueprint(common_route)
app.register_blueprint(doctor)

with app.app_context():
    db.create_all()