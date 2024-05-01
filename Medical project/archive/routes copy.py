from flask import render_template,redirect,url_for,flash,request
from framework.forms import register_user_form,login_user_form,register_pharma_form,login_pharma_form,medicine_return_form
from framework import app,db,models,login_manager,MED_UPLOAD_FOLDER,PRE_UPLOAD_FOLDER
from framework.models import users,pharmacy,medicine_request_pool
from flask_login import login_required,LoginManager,login_user,current_user,logout_user
import os


@login_manager.user_loader
def load_user(userid):
    user=users.query.get(int(userid))
    if user:
        return user
    pharma_user=pharmacy.query.get(int(userid))
    return pharma_user


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/sample')
def sample():
    user=current_user
    return render_template('sample.html',user=user)

@app.route('/med_return',methods=['GET','POST'])
def med_return():
    form=medicine_return_form()
    print("hellow")
    pharmacies = pharmacy.query.filter_by(pincode="specific_pincode").all()  
    if form.validate_on_submit():
        print("works")
        prescription_name=form.prescription_name.data
        medicine_image = request.files['medicine_image']
        prescription_image = request.files['prescription_image']
        img_extension1 = os.path.splitext(medicine_image.filename)[1]
        img_extension2 = os.path.splitext(prescription_image.filename)[1]
        pincode="new123"
        r1=medicine_request_pool(prescription_name=prescription_name,userid=current_user.userid,pincode=pincode)
        db.session.add(r1)
        db.session.commit()
        request_id=r1.id
        img_name1 = f"{request_id}{img_extension1}"
        img_name2 = f"{request_id}{img_extension2}"
        medicine_image_path = os.path.join(MED_UPLOAD_FOLDER,img_name1)
        prescription_image_path = os.path.join(PRE_UPLOAD_FOLDER,img_name2)
        medicine_image.save(medicine_image_path)
        prescription_image.save(prescription_image_path)
        flash("this is done","success")
    else:
        print("doesntwork")
    return render_template('med_return.html',form=form)

@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    form=register_user_form()
    if form.validate_on_submit():
        create_user = users(fname = form.fname.data,
                            lname = form.lname.data,
                            username = form.username.data,
                            email = form.email.data,
                            password = form.password.data)
        
        user=users.query.filter_by(email=create_user.email).first()
        if user :
            flash("account already exists","general")
            return render_template("register_user.html",form=form)
        db.session.add(create_user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template('register_user.html',form=form)

@app.route('/register_pharma', methods=['GET', 'POST'])
def register_pharma():
    form=register_pharma_form()
    if form.validate_on_submit():
        fname=form.fname.data
        lname=form.lname.data
        email=form.email.data
        pharma=pharmacy.query.filter_by(email=email).first()
        if pharma :
            flash("Email already exists","general")
            return render_template("register_pharma.html",form=form)
        password=form.password.data
        new_user=pharmacy(fname=fname,lname=lname,email=email)
        new_user.set_pass(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login_pharma"))
    return render_template('register_pharma.html',form=form)

@app.route('/login_pharma', methods=['POST','GET'])
def login_pharma():
    form=login_pharma_form()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        user=pharmacy.query.filter_by(email=email).first()
        if user :
            if user.check_pass(password):
                login_user(user)
                return redirect(url_for("home"))
            else:
                flash("Wrong password","general")
                return redirect(url_for("login_users"))
        flash("User doesnt exists","general")
        return redirect(url_for("login_pharma"))
    return render_template('login_pharma.html',form=form)

@app.route('/login_users', methods=['POST','GET'])
def login_users():
    login_form = login_user_form()
    register_form = register_user_form()
    
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = users.query.filter_by(email=email).first()
        if user:
            if user.check_pass(password):
                login_user(user)
                return redirect(url_for("sample"))
            else:
                flash("Wrong password","general")
                return redirect(url_for("login_users"))
        flash("User doesn't exist","general")
        return redirect(url_for("login_users"))
    
    return render_template('login_users.html', login_form=login_form, register_form=register_form)
