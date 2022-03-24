from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False, unique=False)
    is_patient = db.Column(db.Boolean, default=False)
    is_technician = db.Column(db.Boolean, default=False)
    is_doctor = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, public_id=None, is_patient=False, is_technician=False, is_doctor=False):
        self.username = username
        self.password = password
        self.public_id = public_id
        self.is_patient = is_patient
        self.is_technician = is_technician
        self.is_doctor = is_doctor

    def __repr__(self):
        return f"{self.username}"


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return f'{self.name}'


class Analysis(db.Model):
    __tablename__ = 'analysis'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref='analyzes')
    name = db.Column(db.String, nullable=False)
    orders = db.relationship('Order', backref='analysis')
    __table_args__ = (db.UniqueConstraint(category_id, name),)

    def __repr__(self):
        return f'{self.category.name}: {self.name}'


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'), nullable=False)
    result = db.Column(db.Text, nullable=True)
    doctors = relationship('DoctorOrder', uselist=True, backref='orders')

    def __repr__(self):
        return f'Order №{self.id} ** Patient: {self.user.username} ** Analysis: {self.analysis.name}'


class DoctorOrder(db.Model):
    __tablename__ = 'doctor_orders'

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    doctor = relationship('User', backref='orders')
