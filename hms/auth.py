from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .extn import db
from .model import User
from .send_mail import send_mail

auth = Blueprint('auth', __name__)


def check_login():
    if 'user_id' in session:
        if session['user_type'] == 'PATIENT':
            return 'patient.dashboard'

        if session['user_type'] == 'DOCTOR':
            return 'doctor.dashboard'

        if session['user_type'] == 'ADMIN_G':
            return 'admin_g.dashboard'

        if session['user_type'] == 'ADMIN_D':
            return 'admin_d.dashboard'

    return None


@auth.route('/', methods=['GET', 'POST'])
def patient_login():

    chk_login = check_login()
    if chk_login:
        return redirect(url_for(chk_login))

    if request.method == "POST":
        data = request.form.to_dict(flat=True)

        user = User.query.filter_by(email=data['email']).first()

        if not user or user.user_type != "PATIENT":
            flash("No Account Found!")
            return redirect(url_for('auth.patient_login'))

        if user.password != data['password']:
            flash("Invalid Password!")
            return redirect(url_for('auth.patient_login'))

        session['user_id'] = user.id
        session['user_type'] = user.user_type

        return redirect(url_for('patient.dashboard'))

    return render_template('./auth/patient_login.html')


@auth.route('/patient_register', methods=['GET', 'POST'])
def patient_register():

    chk_login = check_login()
    if chk_login:
        return redirect(url_for(chk_login))

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        check_email = User.query.filter_by(email=data['email']).first()
        if check_email:
            flash("Email Address Already Registered!")
            return redirect(url_for('auth.patient_register'))

        user = User(
            fname=data['fname'],
            lname=data['lname'],
            email=data['email'],
            password=data['password'],
            contact=data['contact'],
            gender=data['gender'],
            user_type='PATIENT'
        )

        try:
            db.session.add(user)
            db.session.commit()
        except:
            flash("Database Error")

        session['user_id'] = user.id
        session['user_type'] = user.user_type

        return redirect(url_for('patient.dashboard'))
    return render_template('./auth/patient_register.html')


@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():

    chk_login = check_login()
    if chk_login:
        return redirect(url_for(chk_login))

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        user = User.query.filter_by(email=data['email']).first()

        send_mail("Password Recovery", user.email, user.password)

        flash(f"Password Sent To {user.email}")
        return redirect(url_for('auth.forgot_password'))

    return render_template('./auth/forgot_password.html')


@auth.route('/doctor_login', methods=['GET', 'POST'])
def doctor_login():

    chk_login = check_login()
    if chk_login:
        return redirect(url_for(chk_login))

    if request.method == "POST":
        data = request.form.to_dict(flat=True)

        user = User.query.filter_by(username=data['username']).first()

        if not user or user.user_type != "DOCTOR":
            flash("No Account Found!")
            return redirect(url_for('auth.doctor_login'))

        if user.password != data['password']:
            flash("Invalid Password!")
            return redirect(url_for('auth.doctor_login'))

        session['user_id'] = user.id
        session['user_type'] = user.user_type

        return redirect(url_for('doctor.dashboard'))

    return render_template('./auth/doctor_login.html')


@auth.route('/admin_general_login', methods=['GET', 'POST'])
def admin_g_login():

    chk_login = check_login()
    if chk_login:
        return redirect(url_for(chk_login))

    if request.method == "POST":
        data = request.form.to_dict(flat=True)

        user = User.query.filter_by(username=data['username']).first()

        if not user or user.user_type != "ADMIN_G":
            flash("No Account Found!")
            return redirect(url_for('auth.admin_g_login'))

        if user.password != data['password']:
            flash("Invalid Password!")
            return redirect(url_for('auth.admin_g_login'))

        session['user_id'] = user.id
        session['user_type'] = user.user_type

        return redirect(url_for('admin_g.dashboard'))

    return render_template('./auth/admin_g_login.html')


@auth.route('/admin_doctor_login', methods=['GET', 'POST'])
def admin_d_login():

    chk_login = check_login()
    if chk_login:
        return redirect(url_for(chk_login))

    if request.method == "POST":
        data = request.form.to_dict(flat=True)

        user = User.query.filter_by(username=data['username']).first()

        if not user or user.user_type != "ADMIN_D":
            flash("No Account Found!")
            return redirect(url_for('auth.admin_d_login'))

        if user.password != data['password']:
            flash("Invalid Password!")
            return redirect(url_for('auth.admin_d_login'))

        session['user_id'] = user.id
        session['user_type'] = user.user_type

    return render_template('./auth/admin_d_login.html')


@auth.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
        session.pop('user_type')

        return redirect(url_for('auth.patient_login'))