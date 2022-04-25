import jwt
import uuid
from flask import Flask, jsonify, make_response, request
from functools import wraps
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

from project.models import db, Category, Analysis, User, Order, DoctorOrder
from project.schemas import ma, categories_schema, order_schema, orders_schema


app = Flask(__name__)
app.config.from_object('project.config.Config')
db.init_app(app)
ma.init_app(app)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'message': 'Token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid'})
        return f(current_user, *args, **kwargs)

    return decorator


def role_required(role=None):
    @wraps(role)
    def wrap(f):
        @wraps(f)
        def decorator(current_user):
            if getattr(current_user, f'is_{role}'):
                return f(current_user)
            return make_response('Forbidden', 403)
        return decorator
    return wrap


@app.route('/login', methods=['POST'])
def login():
    auth = request.form
    username = auth.get('username')
    password = auth.get('password')

    if not (auth or username or password):
        return make_response('Username and password are required', 403)

    user = User.query.filter_by(username=username).first()

    if not user:
        return make_response('User does not exist', 403)

    if check_password_hash(user.password, password):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.utcnow() + timedelta(days=7)}, app.config['SECRET_KEY']
        )

        return make_response(jsonify({'token': token}), 201)

    return make_response('Wrong password', 403)


@app.route('/signup', methods=['POST'])
def signup():
    data = request.form

    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return make_response('Username and password required', 400)

    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(public_id=str(uuid.uuid4()), username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        return make_response('Successfully registered', 201)
    else:
        return make_response(f'User `{username}` already exists. Please Log in.', 202)


@app.route('/analyses', methods=['GET', 'POST'])
@token_required
@role_required('patient')
def analyses(current_user):
    if request.method == 'GET':
        categories = Category.query.all()
        return categories_schema.jsonify(categories)
    else:
        analysis_id = request.form['analysis_id']
        doctors_ids = request.form.getlist('doctors_ids')
        analysis = Analysis.query.filter_by(id=int(analysis_id)).first()

        if analysis:
            order = Order(user_id=current_user.id, analysis_id=analysis.id)
            db.session.add(order)
            db.session.flush()
            db.session.refresh(order)

            if doctors_ids:
                wrong_doctors_ids = []
                for doctor_id in doctors_ids:
                    doctor = User.query.filter_by(id=int(doctor_id), is_doctor=True).first()
                    if doctor:
                        db.session.add(DoctorOrder(doctor_id=doctor_id, order_id=order.id))
                    else:
                        wrong_doctors_ids.append(doctor_id)
                if wrong_doctors_ids:
                    db.session.rollback()
                    return make_response(f'Doctors with ids {*wrong_doctors_ids,} don\'t exist', 404)

            db.session.commit()
            return make_response('', 201)

        return make_response('Analysis is not exists', 404)


@app.route('/fill_result', methods=['PATCH'])
@token_required
@role_required('technician')
def fill_result(current_user):
    order_id = request.form['order_id']
    result = request.form['result']
    order = Order.query.filter_by(id=int(order_id)).first()

    if not result:
        return make_response('Result can\'t be empty', 404)

    if not order:
        return make_response('Order is not exists', 404)

    order.result = result
    db.session.commit()
    return order_schema.jsonify(order)


@app.route('/doctor_orders', methods=['GET'])
@token_required
@role_required('doctor')
def doctor_orders(current_user):
    orders_ids = [order.id for order in DoctorOrder.query.filter_by(doctor_id=current_user.id).all()]
    results = Order.query.filter(Order.id.in_(orders_ids)).all()
    return orders_schema.jsonify(results)
