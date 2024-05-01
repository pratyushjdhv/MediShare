from framework import db,bcrypt
from framework import login_manager
from flask_login import UserMixin
from sqlalchemy import ForeignKey

class users(db.Model, UserMixin):
    userid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(35), nullable=False)  
    fullname = db.Column(db.String(35), nullable=False)
    email = db.Column(db.String(320), nullable=False, unique=True)
    hashed_password = db.Column(db.String(length=65), nullable=False)  
    pincode=db.Column(db.String(6), default='000000')
    
    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, plain_text_password):
        self.hashed_password = bcrypt.generate_password_hash(plain_text_password).decode('utf8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.hashed_password, attempted_password)

    def get_id(self):
        return str(self.userid) # Convert to string because Flask-Login expects a string ID
    
    def is_pharma(self):
        return False

    

class pharmacy(db.Model,UserMixin):
    pharmaid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    license_no = db.Column(db.String(12))
    pharma_name=db.Column(db.String(65))
    pincode = db.Column(db.Integer, nullable=False)
    email=db.Column(db.String(320),nullable=False)
    hashed_password=db.Column(db.String(length=65),nullable=False)
    address = db.Column(db.String(256), nullable=False)

    @property
    def password(self):
        return self.hashed_password
    
    @password.setter
    def password(self, plain_text_password):
        self.hashed_password = bcrypt.generate_password_hash(plain_text_password).decode('utf8')
        
    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.hashed_password, attempted_password)
    
    def get_id(self):
        return str(self.pharmaid) # Convert to string because Flask-Login expects a string ID
    
    def is_pharma(self):
        return self.is_pharmacist


'''class pharma_address(db.Model,UserMixin):
    address_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    license_no=db.Column(db.String(12),ForeignKey('pharmacy.license_no'))
    state=db.Column(db.String(35))
    district=db.Column(db.String(35))
    city=db.Column(db.String(35))
    pincode=db.Column(db.String(6))
    street_address=db.Column(db.String(200))'''
    
class medicine_request_pool(db.Model,UserMixin):
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    userid=db.Column(db.Integer)
    prescription_name=db.Column(db.String(100))
    pincode=db.Column(db.String(6), default='000000')
    medications = db.Column(db.String(2000))

class meds_scheduler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),db.ForeignKey(users.username) ,nullable=False)
    dosage = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.String(50), nullable=False)    
    user_id = db.Column(db.Integer, db.ForeignKey(users.userid), nullable=False)
    notes = db.Column(db.Text, nullable=True)
