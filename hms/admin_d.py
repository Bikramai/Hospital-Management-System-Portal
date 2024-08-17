from flask import Blueprint, render_template, redirect, url_for, flash, abort,session, request
from .model import Appointment, User, Specialization

admin_d = Blueprint('admin_d', __name__, url_prefix='/admin_d')


@admin_d.before_request
def check_user_type():
    if 'user_id' not in session:
        return redirect(url_for('auth.admin_d_login'))

    if session['user_type'] in ['PATIENT', 'DOCTOR', 'ADMIN_G']:
        return abort(403)


@admin_d.route('/')
def dashboard():

    user = User.query.filter_by(id=session['user_id']).first()

    return render_template('./admin_d/dashboard.html'
                           , user=user)


@admin_d.route('/view_doctors')
def view_doctors():

    search = request.args.get('search_email', None, type=str)

    user = User.query.get(session['user_id'])

    doctors = User.query.filter(User.user_type=="DOCTOR")

    if search:
        doctors = doctors.filter(User.email==search)

    doctors = doctors.all()

    return render_template('./view_doctor.html'
                           , user=user
                           , doctors=doctors)


@admin_d.route('/view_patients')
def view_patients():

    search = request.args.get('search_contact', None, type=str)

    user = User.query.get(session['user_id'])

    patients = User.query.filter(User.user_type=="PATIENT")

    if search:
        patients = patients.filter(User.contact==search)

    patients = patients.all()

    return render_template('./view_patient.html'
                           , user=user
                           , patients=patients)


@admin_d.route('/appointment_details')
def appointment_details():

    user = User.query.get(session['user_id'])

    search = request.args.get('search_contact', None, type=str)

    appt = Appointment.query

    if search:
        appt = appt.filter(User.contact==search)

    appt = appt.all()

    return render_template('./admin_d/appointment_details.html'
                           , user=user
                           , appointments=appt)


@admin_d.route('/prescription_list')
def prescription_list():
    user = User.query.get(session['user_id'])

    appt = Appointment.query.filter(Appointment.status=="Prescribed").all()

    return render_template('./admin_d/prescription_list.html'
                           , user=user
                           , appointments=appt)