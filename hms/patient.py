from flask import Blueprint, render_template, session, request, redirect, url_for, abort, flash
from .model import User, Specialization, Appointment
from .extn import db, SPECIALIZATIONS

patient = Blueprint('patient', __name__, url_prefix='/patient')


@patient.before_request
def check_user_type():
    if 'user_id' not in session:
        return redirect(url_for('auth.patient_login'))

    if session['user_type'] in ['DOCTOR', 'ADMIN_G', 'ADMIN_D']:
        return abort(403)


@patient.route('/')
def dashboard():
    user = User.query.get(session['user_id'])

    return render_template("./patient/dashboard.html"
                           , user=user)


@patient.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        appointment = Appointment(
            doctor_id=data['doctor_id'],
            patient_id=session['user_id'],
            appointment_date=data['appoint_date'],
            appointment_time=data['appoint_time'],
            fee=data['fee'],
            status='Active'
        )

        try:
            db.session.add(appointment)
            db.session.commit()
        except:
            print('Error')

        flash(f"Appointment Booked")

        return redirect(url_for('patient.book_appointment'))

    spec = request.args.get('specialization', None, type=str)
    doc = request.args.get('doctor', None, type=int)

    user = User.query.get(session['user_id'])

    doctor = list()
    if spec:
        doctor = Specialization.query.filter_by(specialize=spec).all()

    return render_template('./patient/book-appointment.html'
                           , user=user
                           , specializations=SPECIALIZATIONS
                           , selected_spec=spec
                           , doctor=doctor if doctor else None
                           , selected_doctor=doc)


@patient.route('/appointment_history')
def appointment_history():
    user = User.query.get(session['user_id'])

    appt = Appointment.query.filter_by(patient_id=session['user_id']).all()

    return render_template('./patient/appointment_history.html'
                           , user=user
                           , appointments=appt)


@patient.route('/prescriptions')
def prescriptions():
    user = User.query.get(session['user_id'])

    appt = Appointment.query.filter(Appointment.patient_id == session['user_id']). \
        filter(Appointment.status == 'Prescribed').all()

    return render_template('./patient/prescriptions.html'
                           , user=user
                           , appointments=appt)


@patient.route('/cancel_appointment/<int:appointment_id>')
def cancel_appointment(appointment_id):
    appt = Appointment.query.get(appointment_id)
    if appt.patient_id == session['user_id']:
        appt.status = "Cancelled"
        appt.action = "Cancelled By Patient"

        try:
            db.session.commit()
        except:
            print('Error')

    return redirect(url_for('patient.appointment_history'))
