from flask import render_template, redirect, url_for, flash, request
from framework.forms import *
from framework import app, db, models, login_manager, MED_UPLOAD_FOLDER, PRE_UPLOAD_FOLDER, EQU_UPLOAD_FOLDER, BILL_UPLOAD_FOLDER
from framework.models import *
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
                flash(f'Account created successfully! You are now logged in as {
                      user.username} ', category='success')
                return redirect(url_for("home"))
            else:
                flash("Wrong password", "danger")
                return redirect(url_for("login_users"))
        flash("User doesn't exist", "danger")
        return redirect(url_for("login_users"))
    return render_template('login_users.html', login_form=form1, register_form=form2)

@app.route('/home')
@login_required
def home():
    if current_user.is_pharma:
        return redirect(url_for("pharma_home"))
    if current_user.is_authenticated and current_user.pincode:
        pharmacies = pharmacy.query.filter_by(pincode=current_user.pincode)
        return render_template('home.html', user=current_user, pharmacies=pharmacies)
    return render_template('home.html', current_user=current_user)

@app.route('/profile_page')
@login_required
def profile_page():
    if current_user.is_pharma: 
        return redirect(url_for("pharma_profile_page"))
    pharmacies = pharmacy.query.filter_by(pincode=current_user.pincode)
    pharmacount = pharmacy.query.filter_by(pincode=current_user.pincode).count()
    return render_template('profile_page.html', user=current_user, pharmacies=pharmacies, pharmacount=pharmacount,current_user=current_user)

@app.route('/pharma_profile_page')
@login_required
def pharma_profile_page():
    return render_template('pharma_profile_page.html', current_user=current_user,user=current_user)


@app.route('/view_image', methods=['POST'])
@login_required
def view_image():
    # Retrieve the image path from the form data
    image_path = request.form.get('image_path')

    # Redirect the user to the image URL
    return redirect(image_path)

@app.route('/donate', methods=["POST", "GET"])
@login_required
def donate():
    form = medical_equipment_form()
    if form.validate_on_submit():
        existing_request = donation_box.query.filter_by(
            equip_name=form.equip_name.data,
            userid=current_user.userid,
            pincode=current_user.pincode
        ).first()
        if existing_request:
            flash("Request already exists", "danger")
            return render_template('donate.html', form=form)

        donation = donation_box(
            equip_name=form.equip_name.data,
            userid=current_user.userid,
            pincode=current_user.pincode
        )
        db.session.add(donation)
        db.session.commit()

        equip_image = request.files['equip_image']
        bill_image = request.files['bill_image']
        donation_id = donation.id
        img_ext1 = os.path.splitext(equip_image.filename)[1]
        if bill_image:
            img_ext2 = os.path.splitext(bill_image.filename)[1]
            img_name2 = f"{donation_id}{img_ext2}"
            bill_image_path = os.path.join(BILL_UPLOAD_FOLDER, img_name2)
            bill_image.save(bill_image_path)
        img_name1 = f"{donation_id}{img_ext1}"
        equip_image_path = os.path.join(EQU_UPLOAD_FOLDER, img_name1)
        equip_image.save(equip_image_path)
        flash("This is done", "success")
    return render_template('donate.html', form=form, user=current_user,current_user=current_user)


@app.route('/search_user',methods=["POST","GET"])
@login_required
def search_user():
    userid=request.form.get("userid")
    all_users=users.query.filter_by(userid=userid)
    count=users.query.filter_by(userid=userid).count()
    if count==0:
        flash("User not find", "danger")
    return render_template('pharma_user.html', current_user=current_user,all_user=all_users)

@app.route('/reduce_point',methods=["POST","GET"])
@login_required
def reduce_point():
    userid=request.form.get("userid")
    user=users.query.get(userid)
    rpoints=int(request.form.get("points"))
    if user.points >= rpoints:
        final=user.points-rpoints
        user.points=final
        db.session.commit()
        flash("Points reduced", "success")
    else:
        flash("cannot be reduced", "danger")
    all_users=users.query.filter_by(userid=userid)
    return render_template('pharma_user.html', current_user=current_user,all_user=all_users)

@app.route('/pharma_home')
@login_required
def pharma_home():
    all_request = medicine_request_pool.query.filter_by(
        pharmaid=current_user.get_id())
    return render_template('pharma_home.html', current_user=current_user, all_request=all_request, MED_UPLOAD_FOLDER=MED_UPLOAD_FOLDER, PRE_UPLOAD_FOLDER=PRE_UPLOAD_FOLDER)

@app.route('/request_his')
@login_required
def request_his():
    all_request = medicine_request_pool.query.filter_by(userid=current_user.get_id())
    return render_template('request_his.html', current_user=current_user, all_request=all_request)

@app.route('/pharma_user')
@login_required
def pharma_user():
    all_user=users.query.all()
    return render_template('pharma_user.html', current_user=current_user,all_user=all_user)


'''@app.route('/test')
def test():
    return f"Current user: {current_user.username}'''


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login_users'))


@app.route("/add_points", methods=["POST"])
@login_required
def add_points():
    if request.method == 'POST':
        userid=request.form.get("userid")
        request_id=request.form.get("request_id")
        request_points=request.form.get("user_points")
        current_request=medicine_request_pool.query.get(request_id)
        current_request.points_given=request_points
        user=users.query.get(userid)
        user.points=request_points
        redirect_url = request.form.get('redirect_url')
        db.session.commit()
    return redirect(redirect_url)


@app.route("/reject", methods=["POST"])
@login_required
def reject():
    if request.method == 'POST':
        request_id = request.form.get("request_id")
        request_reason = request.form.get("rejection_reason")
        current_request = medicine_request_pool.query.get(request_id)
        redirect_url = request.form.get('redirect_url')
        current_request.is_rejected = 1
        current_request.reason = request_reason
        db.session.commit()
    return redirect(redirect_url)


@app.route("/approve", methods=["POST"])
@login_required
def approve():
    if request.method == 'POST':
        request_id = request.form.get("request_id")
        current_request = medicine_request_pool.query.get(request_id)
        redirect_url = request.form.get('redirect_url')
        current_request.is_approved = 1
        db.session.commit()
    return redirect(redirect_url)


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



@app.route('/med_return', methods=['GET', 'POST'])
@login_required
def med_return():
    if current_user.pharmaid == 0:
        flash("Please select default pharmacy", "danger")
        return redirect(url_for("profile_page"))
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
            return render_template('med_return.html', form=form,current_user=current_user)

        # Extract multiple medications from form and join them into a single string
        medications_str = ', '.join(request.form.getlist('meds'))

        # Create new request
        requests = medicine_request_pool(
            prescription_name=form.prescription_name.data,
            userid=current_user.userid,
            pincode=current_user.pincode,
            medications=medications_str,
            pharmaid=current_user.pharmaid
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
            pharmacy_name=form2.username.data,
            license_no=form2.license_no.data,
            email=form2.email.data,
            password=form2.password.data,
            pincode=form2.pincode.data,
            address=form2.address.data
        )
        user = pharmacy.query.filter_by(email=create_user.email).first()
        if user:
            flash("account already exists", "general")
            # Correct the redirect URL
            return redirect(url_for("login_pharma"))
        db.session.add(create_user)
        db.session.commit()
        login_user(create_user)
        return redirect(url_for("pharma_home"))
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
                flash(f'Pharmacy Account created successfully! You are now logged in as {user.pharmacy_name}', category='success')
                return redirect(url_for("pharma_home"))
            else:
                flash("Wrong password", "danger")
                return redirect(url_for("login_pharma"))
        flash("User doesn't exist", "danger")
        return redirect(url_for("login_pharma"))
    return render_template('login_pharma.html', login_form=form1, register_form=form2)

# medicine scheduler


@app.route('/med_scheduler', methods=['GET', 'POST'])
@login_required
def med_scheduler():
    form = med_scheduler_form()
    if form.validate_on_submit():
        form.user_id.data = current_user.userid
        print("Form is valid")
        print("Current user ID:", current_user.userid)  # Debugging print
        schedule = meds_scheduler(
            user_id=current_user.userid,  # Use current_user.userid here
            med_name=form.med_name.data,
            dosage=form.dosage.data,
            frequency=form.frequency.data,
            notes=form.notes.data
        )
        # Check if the medicine already exists for the current user
        med = meds_scheduler.query.filter_by(
            user_id=current_user.userid, med_name=form.med_name.data).first()
        if med:
            flash("Medicine already exists", "danger")
            # Redirect instead of rendering the template
            return redirect(url_for('med_scheduler'))
        db.session.add(schedule)
        db.session.commit()
        flash('Medicine scheduled successfully', 'success')
        # Redirect to avoid resubmission on page refresh
        return redirect(url_for('med_scheduler'))
    else:
        print("Form errors:", form.errors)  # Debugging print for form errors
    return render_template('med_scheduler.html', form=form)


@app.route("/change_pincode", methods=["POST"])
@login_required
def change_pincode():
    if request.method == 'POST':
        pincode = request.form.get("new_pincode")
        current_user.pincode = pincode
        redirect_url = request.form.get('redirect_url')
        db.session.commit()
    return redirect(redirect_url)


@app.route("/select_pharma", methods=["POST", "GET"])
@login_required
def select_pharma():
    if request.method == 'POST':
        id = request.form.get("selected_pharmacy")
        phar = pharmacy.query.get(id)
        address = phar.address
        name = phar.username
        current_user.pharmaid = id
        current_user.address = address
        current_user.pharmacy_name = name
        redirect_url = request.form.get('redirect_url')
        db.session.commit()
    return redirect(redirect_url)
