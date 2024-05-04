from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///medicare_database.sqlite3"
app.config["SECRET_KEY"] = "this_is_a_secret_key"
db = SQLAlchemy(app)
login_manager = LoginManager(app)

MED_UPLOAD_FOLDER = os.path.join(app.static_folder, 'medicine_images')
PRE_UPLOAD_FOLDER =  os.path.join(app.static_folder, 'prescription_images')
EQU_UPLOAD_FOLDER = os.path.join(app.static_folder, 'equip_images')
BILL_UPLOAD_FOLDER = os.path.join(app.static_folder, 'bill_images')


if not os.path.exists(MED_UPLOAD_FOLDER):
    os.makedirs(MED_UPLOAD_FOLDER)

if not os.path.exists(PRE_UPLOAD_FOLDER):
    os.makedirs(PRE_UPLOAD_FOLDER)

login_manager.login_view = "login_users"
login_manager.login_message = "Please log in to access this page."

from framework.models import users, pharmacy


'''@login_manager.user_loader
def load_user(user_id):
    # Check if user is a regular user
    user = users.query.get((user_id))
    if user:
        return user
    # Check if user is a pharmacy user
    pharma_user = pharmacy.query.get((user_id))
    if pharma_user:
        return pharma_user
    return None  # Return None if user ID is not found'''

@login_manager.user_loader
def load_user(user_id):
    # Convert user_id back to integer since it's stored as an integer in the database
    user_id = int(user_id)
    user = users.query.get(user_id)
    if user:        
        return user
    pharma_user = pharmacy.query.get(user_id)
    if pharma_user:        
        return pharma_user
    return None # Return None if user ID is not found

from framework.routes import *

with app.app_context():
    db.create_all()
