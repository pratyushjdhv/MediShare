from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField, FileField,SelectField
from wtforms import StringField,EmailField,PasswordField,FileField
from wtforms.validators import DataRequired,Email,Length,equal_to
from flask_wtf.file import FileAllowed

class register_user_form(FlaskForm):  
    username=StringField("First Name :",validators=[DataRequired(message="Cannot be empty"),Length(max=35,message="Too long!")])
    fullname=StringField("First Name :",validators=[DataRequired(message="Cannot be empty"),Length(max=35,message="Too long!")])
    email = EmailField("Email :", validators=[DataRequired(message="Cannot be empty",), Email(message="Enter a valid email"),Length(max=320,message="Too long!")])
    password=PasswordField("Password :",validators=[DataRequired(message="Cannot be empty"),Length(min=8,message="Should atleast contain 8 character!"),Length(max=80,message="Too long!")])
    cpassword=PasswordField("Confirm Password :",validators=[DataRequired(message="Cannot be empty"),equal_to("password",message="Both password field must be equal!")])
    pincode=StringField("Pincode :",validators=[DataRequired(message="Cannot be empty"),Length(min=6,max=6,message="Should be 6 digit!")])

class login_user_form(FlaskForm):
    email = EmailField("Email :", validators=[DataRequired(message="Cannot be empty",), Email(message="Enter a valid email"),Length(max=320,message="Too long!")])
    password=PasswordField("Password :",validators=[DataRequired(message="Cannot be empty"),Length(min=8,message="Should atleast contain 8 character!"),Length(max=80,message="Too long!")])

class register_pharma_form(FlaskForm):
    license_no=StringField("First Name :",validators=[DataRequired(message="Cannot be empty"),Length(max=12,message="Too long!")])
    pharma_name=StringField("First Name :",validators=[DataRequired(message="Cannot be empty"),Length(max=35,message="Too long!")])
    pincode=StringField("Pincode :",validators=[DataRequired(message="Cannot be empty"),Length(min=6,max=6,message="Should be 6 digit!")])
    email = EmailField("Email :", validators=[DataRequired(message="Cannot be empty",), Email(message="Enter a valid email"),Length(max=320,message="Too long!")])
    password=PasswordField("Password :",validators=[DataRequired(message="Cannot be empty"),Length(min=8,message="Should atleast contain 8 character!"),Length(max=80,message="Too long!")])
    cpassword=PasswordField("Confirm Password :",validators=[DataRequired(message="Cannot be empty"),equal_to("password",message="Both password field must be equal!")])
    address=StringField("Address :",validators=[DataRequired(message="Cannot be empty"),Length(max=256,message="Too long!")])


class medicine_return_form(FlaskForm):
    medicine_image = FileField("Medicine Image:", validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    prescription_name = StringField("Prescription Name:", validators=[DataRequired(message="Cannot be empty"), Length(max=100, message="Too long!")])
    prescription_image = FileField("Prescription Image:", validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    meds = StringField("Medications 1:", validators=[DataRequired(message="Cannot be empty")])
    

class login_pharma_form(FlaskForm):
    email = EmailField("Email :", validators=[DataRequired(message="Cannot be empty",), Email(message="Enter a valid email"),Length(max=320,message="Too long!")])
    password=PasswordField("Password :",validators=[DataRequired(message="Cannot be empty"),Length(min=8,message="Should atleast contain 8 character!"),Length(max=80,message="Too long!")])

class med_scheduler_form(FlaskForm):
    med_name = StringField("Medicine Name :",validators=[DataRequired(message="Cannot be empty"),Length(max=100,message="Too long!")])
    dosage = StringField("Dosage :",validators=[DataRequired(message="Cannot be empty"),Length(max=50,message="Too long!")])
    frequency = StringField("Frequency :",validators=[DataRequired(message="Cannot be empty"),Length(max=50,message="Too long!")])
    submit = SubmitField("Submit")