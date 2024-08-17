from flask import Blueprint, render_template, session, redirect, url_for, request, abort, flash
from .model import Appointment, User, Contact
from .extn import db

common_route = Blueprint('common_route', __name__)


@common_route.route('/search', methods=['GET', 'POST'])
def search():

    if session['user_type'] == "PATIENT":
        return redirect(url_for('patient.dashboard'))

    appt = None
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        appt = Appointment.query.filter(Appointment.doctor_id==session['user_id']).filter(User.email==data['email']).all()

    return render_template("./search.html"
                           , appointment=appt)


@common_route.route('/contact_us', methods=['GET', 'POST'])
def contact_us():

    if 'user_id' in session:
        return abort(403)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        contact = Contact(
            name=data['name'],
            email=data['email'],
            contact=data['contact'],
            message=data['message']
        )

        try:
            db.session.add(contact)
            db.session.commit()
        except:
            print("Error")

        flash("Thankyou for contacting us!")
        return redirect(url_for('common_route.contact_us'))

    return render_template('./contact-us.html')