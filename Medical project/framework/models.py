from framework import db, bcrypt
from framework import login_manager
from flask_login import UserMixin
from sqlalchemy import ForeignKey


class users(db.Model, UserMixin):
    """
    Represents a user in the system.

    Attributes:
        userid (int): The unique identifier for the user.
        username (str): The username of the user.
        fullname (str): The full name of the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password of the user.
        pincode (str): The pincode of the user.
        pharmacy_name (str): The name of the pharmacy associated with the user.
        pharmaid (int): The unique identifier for the pharmacy.
        address (str): The address of the user.
        points (int): The number of points the user has.

    Methods:
        password (property): Gets the hashed password of the user.
        password (setter): Sets the hashed password of the user.
        check_password: Checks if the provided password matches the user's hashed password.
        get_id: Gets the string representation of the user's ID.
    """
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
    """
    Represents a pharmacy in the system.

    Attributes:
        pharmaid (int): The unique identifier for the pharmacy.
        license_no (str): The license number of the pharmacy.
        username (str): The username of the pharmacy.
        pincode (int): The pincode of the pharmacy's location.
        email (str): The email address of the pharmacy.
        hashed_password (str): The hashed password of the pharmacy.
        address (str): The address of the pharmacy.

    Methods:
        password (property): Gets the hashed password of the pharmacy.
        password (setter): Sets the hashed password of the pharmacy.
        check_password: Checks if the provided password matches the hashed password of the pharmacy.
        get_id: Gets the string representation of the pharmacy's ID.
    """
    pharmaid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    license_no = db.Column(db.String(12))
    username = db.Column(db.String(65))
    pincode = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(320), nullable=False)
    hashed_password = db.Column(db.String(length=65), nullable=False)
    address = db.Column(db.String(256), nullable=False)

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
    """
    Represents a medicine request in the pool.

    Attributes:
        id (int): The unique identifier for the medicine request.
        userid (int): The user ID associated with the medicine request.
        prescription_name (str): The name of the prescription.
        pincode (str): The pincode associated with the medicine request.
        medications (str): The list of medications requested.
        is_rejected (bool): Indicates if the request has been rejected.
        is_approved (bool): Indicates if the request has been approved.
        reason (str): The reason for rejection or unknown reason.
        pharmaid (int): The ID of the pharmacy assigned to the request.
        points_given (int): The number of points assigned for the request.
    """
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
    """
    Represents a medication scheduler.

    Attributes:
        id (int): The unique identifier for the medication scheduler.
        med_name (str): The name of the medication.
        dosage (str): The dosage of the medication.
        frequency (str): The frequency at which the medication should be taken.
        user_id (int): The ID of the user associated with the medication scheduler.
        notes (str): Additional notes or comments about the medication.
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    med_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        users.userid), nullable=False)
    notes = db.Column(db.Text, nullable=True)


class donation_box(db.Model):
    """
    Represents a donation box in the medical project framework.

    Attributes:
        id (int): The unique identifier for the donation box.
        equip_name (str): The name of the equipment in the donation box.
        points_given (int): The number of points given for the donation box.
        userid (int): The user ID associated with the donation box.
        pincode (str): The pincode of the donation box.
        is_rejected (bool): A boolean value indicating if the donation box is rejected.
        is_approved (bool): A boolean value indicating if the donation box is approved.
        reason (str): The reason for rejection or unknown if not specified.
        pharmaid (int): The pharmacy ID associated with the donation box.
    """
    id = db.Column(db.Integer, primary_key=True)
    equip_name = db.Column(db.String(100))
    points_given = db.Column(db.Integer, default=0)
    userid = db.Column(db.Integer)
    pincode = db.Column(db.String(6), default='000000')
    is_rejected = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    reason = db.Column(db.String(256), default="Not known")
    pharmaid = db.Column(db.Integer, default=1)
