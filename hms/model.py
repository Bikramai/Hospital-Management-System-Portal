from .extn import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), nullable=True)
    contact = db.Column(db.String(20))
    password = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)

    specialization = db.relationship('Specialization', backref='user')

    docAppoint = db.relationship('Appointment', backref='doctor', lazy='dynamic', foreign_keys='Appointment.doctor_id')
    patientAppoint = db.relationship('Appointment', backref='patient', lazy='dynamic', foreign_keys='Appointment.patient_id')

    def __repr__(self):
        return f"<User>: {self.id} - {self.fname} - {self.user_type}"


class Specialization(db.Model):
    __tablename__ = "specialization"
    id = db.Column(db.Integer, primary_key=True)

    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    specialize = db.Column(db.String(20), nullable=False)

    fee = db.Column(db.Integer, nullable=False)

    def get_specialization(self):
        return self.specialize

    def __repr__(self):
        return f"<Specialization>: {self.id} - {self.doctor_id} - {self.specialize}"


class Appointment(db.Model):
    __tablename__ = "appointment"
    id = db.Column(db.Integer, primary_key=True)

    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)

    fee = db.Column(db.Integer, nullable=False)

    action = db.Column(db.String(20))
    status = db.Column(db.String(10))

    disease = db.Column(db.Text)
    allergy = db.Column(db.Text)
    prescription = db.Column(db.Text)

    def __repr__(self):
        return f"<Appointment>: {self.doctor_id} - {self.patient_id}"


class Contact(db.Model):
    __tablename__ = "contact"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(20))
    email = db.Column(db.String(20))
    contact = db.Column(db.String(20))
    message = db.Column(db.Text)

    def __repr__(self):
        return f"<Contact>: {self.name} - {self.email}"