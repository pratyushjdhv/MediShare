from flask import render_template, redirect, url_for, flash, request
from framework.forms import *
from framework import app, db, models, login_manager, MED_UPLOAD_FOLDER, PRE_UPLOAD_FOLDER
from framework.models import users, pharmacy, medicine_request_pool
from flask_login import login_required, LoginManager, login_user, current_user, logout_user
import os

'''
@login_manager.user_loader
def load_user(user_id):
    if user:
        user = users.query.get(int(user_id))    
        return user
    pharma_user = pharmacy.query.get(int(user_id))
    return pharma_user
'''
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', current_user=current_user)

@app.route('/pharma_home')
def pharma_home():
    return render_template('home.html', current_user=current_user)

@app.route('/test')
def test():
    return f"Current user: {current_user.username}"

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    form1 = login_user_form()
    form2 = register_user_form()  # Use register_user_form here
    if form2.validate_on_submit():
        create_user = users(
            fullname=form2.fullname.data,
            username=form2.username.data,
            email=form2.email.data,
            password=form2.password.data,
            pincode=form2.pincode.data
        )
        user = users.query.filter_by(email=create_user.email).first()
        if user:
            flash("account already exists", "general")
            return redirect(url_for("login_user"))  # Correct the redirect URL
        db.session.add(create_user)
        db.session.commit()
        login_user(create_user)
        return redirect(url_for("home"))
    # Pass only register_form to the template
    return render_template('login_users.html', login_form=form1, register_form=form2)


@app.route('/login_users', methods=['POST', 'GET'])
def login_users():
    form1 = login_user_form()
    form2 = register_user_form()
    if form1.validate_on_submit():
        email = form1.email.data
        password = form1.password.data
        user = users.query.filter_by(email=email).first()
        if user:
            if user.check_password(password):
                login_user(user)                
                flash(f'Account created successfully! You are now logged in as {user.username} ', category='success')
                return redirect(url_for("home"))
            else:
                flash("Wrong password", "danger")
                return redirect(url_for("login_users"))
        flash("User doesn't exist", "danger")
        return redirect(url_for("login_users"))
    return render_template('login_users.html', login_form=form1, register_form=form2)


@app.route('/med_return', methods=['GET', 'POST'])
@login_required
def med_return():
    form = medicine_return_form()    
    pharmacies = pharmacy.query.filter_by(pincode=current_user.pincode).all()
    if form.validate_on_submit():
        # Check if the request already exists
        existing_request = medicine_request_pool.query.filter_by(
            prescription_name=form.prescription_name.data,
            userid=current_user.userid,
            pincode=current_user.pincode
        ).first()

        if existing_request:
            flash("Request already exists", "danger")
            return render_template('med_return.html', form=form)
        
        # Extract multiple medications from form and join them into a single string
        medications_str = ', '.join(request.form.getlist('meds'))

        # Create new request
        requests = medicine_request_pool(
            prescription_name=form.prescription_name.data,
            userid=current_user.userid,
            pincode=current_user.pincode,
            medications=medications_str
        )
        db.session.add(requests)
        db.session.commit()
        
        medicine_image = request.files['medicine_image']
        prescription_image = request.files['prescription_image']
        img_extension1 = os.path.splitext(medicine_image.filename)[1]
        img_extension2 = os.path.splitext(prescription_image.filename)[1]
        
        request_id = requests.id
        img_name1 = f"{request_id}{img_extension1}"
        img_name2 = f"{request_id}{img_extension2}"
        medicine_image_path = os.path.join(MED_UPLOAD_FOLDER, img_name1)
        prescription_image_path = os.path.join(PRE_UPLOAD_FOLDER, img_name2)
        medicine_image.save(medicine_image_path)
        prescription_image.save(prescription_image_path)
        flash("This is done", "success")
    return render_template('med_return.html', form=form)


@app.route('/register_pharma', methods=['GET', 'POST'])
def register_pharma():
    form1 = login_user_form()
    form2 = register_pharma_form()  # Use register_user_form here
    if form2.validate_on_submit():
        create_user = pharmacy(
            pharma_name=form2.pharma_name.data,
            license_no=form2.license_no.data,
            email=form2.email.data,
            password=form2.password.data,
            pincode=form2.pincode.data,
            address=form2.address.data
            )
        user = pharmacy.query.filter_by(email=create_user.email).first()
        if user:
            flash("account already exists", "general")
            return redirect(url_for("login_pharma"))  # Correct the redirect URL
        db.session.add(create_user)
        db.session.commit()
        login_user(create_user)
        return redirect(url_for("home"))
    # Pass only register_form to the template
    return render_template('login_pharma.html', login_form=form1, register_form=form2)


@app.route('/login_pharma', methods=['POST', 'GET'])
def login_pharma():
    form1 = login_pharma_form()
    form2 = register_pharma_form()
    if form1.validate_on_submit():
        email = form1.email.data
        password = form1.password.data
        user = pharmacy.query.filter_by(email=email).first()
        if user:
            if user.check_password(password):
                login_user(user)                
                flash(f'Pharamcy Account created successfully! You are now logged in as {user.pharma_name} ', category='success')
                return redirect(url_for("home"))
            else:
                flash("Wrong password", "danger")
                return redirect(url_for("login_pharma"))
        flash("User doesn't exist", "danger")
        return redirect(url_for("login_pharma"))
    return render_template('login_pharma.html', login_form=form1, register_form=form2)

# mdeicine scheduler
@app.route('/med_scheduler', methods=['GET', 'POST'])
@login_required
def med_scheduler():
    form = med_scheduler_form()
    return render_template('med_scheduler.html', form=form) 
    