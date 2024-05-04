from framework import db, bcrypt
from framework import login_manager
from flask_login import UserMixin
from sqlalchemy import ForeignKey


class users(db.Model, UserMixin):
    
    userid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(35), nullable=False)
    fullname = db.Column(db.String(35), nullable=False)
    email = db.Column(db.String(320), nullable=False, unique=True)
    hashed_password = db.Column(db.String(length=65), nullable=False)
    pincode = db.Column(db.String(6), default='000000')
    pharmacy_name = db.Column(db.String(65))
    pharmaid = db.Column(db.Integer, default=0)
    address = db.Column(db.String(256))
    points = db.Column(db.Integer, default=0)
    is_pharma=db.Column(db.Boolean, default=False)
    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, plain_text_password):
        self.hashed_password = bcrypt.generate_password_hash(
            plain_text_password).decode('utf8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.hashed_password, attempted_password)

    def get_id(self):
        # Convert to string because Flask-Login expects a string ID
        return str(self.userid)


class pharmacy(db.Model, UserMixin):
    
    pharmaid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    license_no = db.Column(db.String(12))
    pharmacy_name = db.Column(db.String(65))
    pincode = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(320), nullable=False)
    hashed_password = db.Column(db.String(length=65), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    is_pharma = db.Column(db.Boolean, default=True)
    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, plain_text_password):
        self.hashed_password = bcrypt.generate_password_hash(
            plain_text_password).decode('utf8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.hashed_password, attempted_password)

    def get_id(self):
        # Convert to string because Flask-Login expects a string ID
        return str(self.pharmaid)


class medicine_request_pool(db.Model, UserMixin):
   
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    userid = db.Column(db.Integer)
    prescription_name = db.Column(db.String(100))
    pincode = db.Column(db.String(6), default='000000')
    medications = db.Column(db.String(2000))
    is_rejected = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    reason = db.Column(db.String(256), default="Not known")
    pharmaid = db.Column(db.Integer, default=0)
    points_given = db.Column(db.Integer, default=0)


class meds_scheduler(db.Model):
  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    med_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        users.userid), nullable=False)
    notes = db.Column(db.Text, nullable=True)


class donation_box(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    equip_name = db.Column(db.String(100))
    points_given = db.Column(db.Integer, default=0)
    userid = db.Column(db.Integer)
    pincode = db.Column(db.String(6), default='000000')
    is_rejected = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    reason = db.Column(db.String(256), default="Not known")
    pharmaid = db.Column(db.Integer, default=1)
