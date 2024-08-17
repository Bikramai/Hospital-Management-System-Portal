from flask import Blueprint, flash,  render_template, session, redirect, url_for, abort, request
from .model import User, Contact, Specialization
from .extn import db, SPECIALIZATIONS

admin_g = Blueprint('admin_g', __name__, url_prefix='/admin_g')


@admin_g.before_request
def check_user_type():
    if 'user_id' not in session:
        return redirect(url_for('auth.admin_g_login'))

    if session['user_type'] in ['PATIENT', 'DOCTOR', 'ADMIN_D']:
        return abort(403)


@admin_g.route('/')
def dashboard():
    user = User.query.get(session['user_id'])
    return render_template('./admin_g/dashboard.html'
                           , user=user)


@admin_g.route('/view_doctors')
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


@admin_g.route('/view_patients')
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


@admin_g.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        user = User.query.filter_by(email=data['email']).first()
        if user:
            flash("Email Already Registered")
            return redirect(url_for('admin_g.add_doctor'))

        user = User.query.filter_by(username=data['username']).first()
        if user:
            flash("Username Already Selected")
            return redirect(url_for('admin_g.add_doctor'))

        user = User(
            fname=data['fname'],
            lname=data['lname'],
            email=data['email'],
            username=data['username'],
            password=data['password'],
            user_type='DOCTOR',
            contact='-',
            gender='male'
        )

        spec = Specialization(
            user=user,
            specialize=data['specialize'],
            fee=data['fee']
        )

        try:
            db.session.add(user)
            db.session.add(spec)
            db.session.commit()

            flash("Doctor Added")
        except Exception as e:
            flash('Database Error')
            print(e)

        return redirect(url_for('admin_g.add_doctor'))

    return render_template('./admin_g/add_doctor.html'
                           , user=user
                           , specializations=SPECIALIZATIONS)


@admin_g.route('/delete_doctor', methods=['GET', 'POST'])
def delete_doctor():
    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        user = User.query.filter_by(email=data['email']).first()

        if not user:
            flash("No account Found!")
            return redirect(url_for('admin_g.delete_doctor'))

        user.user_type = 'DELETED'

        try:
            db.session.commit()
        except:
            print('ERROR')

        flash("Account Deleted")
        return redirect(url_for('admin_g.delete_doctor'))

    return render_template('./admin_g/delete_doctor.html'
                           , user=user)


@admin_g.route('/queries')
def queries():
    user = User.query.get(session['user_id'])

    search = request.args.get('search_contact', None, type=str)

    contacts = Contact.query

    if search:
        contacts = contacts.filter(Contact.contact==search)

    contacts = contacts.all()

    return render_template('./admin_g/queries.html'
                           , user=user
                           , contacts=contacts)
