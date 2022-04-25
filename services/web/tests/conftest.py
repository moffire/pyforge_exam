import jwt
import pytest
import uuid

from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

from project import app
from project.models import db, Analysis, Category, Order, User


def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        session.execute(table.delete())
    session.commit()


@pytest.fixture
def client():
    client = app.test_client()
    with app.app_context():
        yield client
        clear_data(db.session)


@pytest.fixture
def user():
    db.session.add(
        User(
            username='user',
            password=generate_password_hash('password'),
            public_id=str(uuid.uuid4()),
        )
    )
    db.session.commit()
    return User.query.first()


@pytest.fixture
def patient():
    db.session.add(User(
        username='parient',
        password=generate_password_hash('password', method='sha256'),
        public_id=str(uuid.uuid4()),
        is_patient=True
    ))
    db.session.commit()
    return User.query.filter_by(is_patient=True).first()


@pytest.fixture
def patient_token():
    db.session.add(User(
        username='parient',
        password=generate_password_hash('password', method='sha256'),
        public_id=str(uuid.uuid4()),
        is_patient=True
    ))
    db.session.commit()
    patient = User.query.filter_by(is_patient=True).first()
    return jwt.encode(
            {'public_id': patient.public_id, 'exp': datetime.utcnow() + timedelta(days=7)}, app.config['SECRET_KEY']
        )


@pytest.fixture
def doctor():
    db.session.add(User(
        username='doctor',
        password=generate_password_hash('password', method='sha256'),
        public_id=str(uuid.uuid4()),
        is_doctor=True
    ))
    db.session.commit()
    return User.query.filter_by(is_doctor=True).first()


@pytest.fixture
def doctor_token():
    db.session.add(User(
        username='doctor',
        password=generate_password_hash('password', method='sha256'),
        public_id=str(uuid.uuid4()),
        is_doctor=True
    ))
    db.session.commit()
    doctor = User.query.filter_by(is_doctor=True).first()
    return jwt.encode(
            {'public_id': doctor.public_id, 'exp': datetime.utcnow() + timedelta(days=7)}, app.config['SECRET_KEY']
        )


@pytest.fixture
def technician():
    db.session.add(User(
        username='technician',
        password=generate_password_hash('password', method='sha256'),
        public_id=str(uuid.uuid4()),
        is_technician=True
    ))
    db.session.commit()
    return User.query.filter_by(is_technician=True).first()


@pytest.fixture
def technician_token():
    db.session.add(User(
        username='technician',
        password=generate_password_hash('password', method='sha256'),
        public_id=str(uuid.uuid4()),
        is_technician=True
    ))
    db.session.commit()
    technician = User.query.filter_by(is_technician=True).first()
    return jwt.encode(
            {'public_id': technician.public_id, 'exp': datetime.utcnow() + timedelta(days=7)}, app.config['SECRET_KEY']
        )


@pytest.fixture
def order():
    db.session.add(User(username='patient', password=generate_password_hash('password'), is_patient=True))
    db.session.add(Category(name='Category #1'))
    db.session.commit()

    user = User.query.filter_by(username='patient').first()
    category = Category.query.filter_by(name='Category #1').first()

    db.session.add(Analysis(category_id=category.id, name='Analysis #1'))
    db.session.commit()

    analysis = Analysis.query.filter_by(name='Analysis #1').first()

    db.session.add(Order(user_id=user.id, analysis_id=analysis.id))
    db.session.commit()
    return Order.query.filter_by(user_id=user.id, analysis_id=analysis.id).first()
