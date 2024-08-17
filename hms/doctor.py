from flask import Blueprint, render_template, session, redirect, url_for, request, abort, flash
from .extn import db
from .model import User, Appointment

doctor = Blueprint('doctor', __name__, url_prefix='/doctor')


@doctor.before_request
def check_user_type():
    if 'user_id' not in session:
        return redirect(url_for('auth.doctor_login'))

    if session['user_type'] in ['PATIENT', 'ADMIN_G', 'ADMIN_D']:
        return abort(403)


@doctor.route('/')
def dashboard():

    user = User.query.get(session['user_id'])

    return render_template('./doctor/dashboard.html'
                           , user=user)


@doctor.route('/view_appointments')
def view_appointments():
    user = User.query.get(session['user_id'])

    appointments = Appointment.query.filter_by(doctor_id=session['user_id']).all()

    return render_template('./doctor/view_appointment.html'
                           , user=user
                           , appointments=appointments)


@doctor.route('/cancel_appointment/<int:appointment_id>')
def cancel_appointment(appointment_id):

    appt = Appointment.query.get(appointment_id)
    if appt.doctor_id == session['user_id']:
        appt.status = "Cancelled"
        appt.action = "Cancelled By Doctor"

        try:
            db.session.commit()
        except:
            print('Error')

    return redirect(url_for('doctor.view_appointments'))


@doctor.route('/prescribe/<int:appointment_id>', methods=['GET', 'POST'])
def prescribe(appointment_id):

    appt = Appointment.query.get(appointment_id)

    if appt.doctor_id != session['user_id']:
        return redirect(url_for('doctor.view_appointments'))

    if appt.status == 'Prescribed':
        flash("Appointment Already Prescribed")
        return redirect(url_for('doctor.view_appointments'))

    if request.method == "POST":

        data = request.form.to_dict(flat=True)

        appt.disease = data['disease']
        appt.allergy = data['allergy']
        appt.prescription = data['prescription']
        appt.status = 'Prescribed'
        appt.action = 'Prescribed By Doctor'

        try:
            db.session.commit()
        except:
            print("Error")

        return redirect(url_for('doctor.view_appointments'))

    return render_template('./doctor/prescribe.html'
                           , appointment=appt)


@doctor.route('/view_prescription')
def view_prescription():
    user = User.query.get(session['user_id'])

    pres = Appointment.query.filter(Appointment.doctor_id == session['user_id']).\
        filter(Appointment.status == 'Prescribed').all()

    return render_template('./doctor/view_prescription.html'
                           , user=user
                           , prescriptions=pres)