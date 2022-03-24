import uuid
from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash

from project import app, db, Category, Analysis, User


cli = FlaskGroup(app)


@cli.command('create_db')
def create_db():
    """
    Create project db
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('seed_db')
def seed_db():
    """
    Populate db with data
    """
    if db.session.query(Category).count() == 0:
        db.session.add(Category(name='Category #1'))
        db.session.add(Category(name='Category #2'))
        db.session.add(Category(name='Category #3'))
        db.session.commit()

    if db.session.query(Analysis).count() == 0:
        category_1 = Category.query.filter_by(name='Category #1').first()
        category_2 = Category.query.filter_by(name='Category #2').first()
        category_3 = Category.query.filter_by(name='Category #3').first()

        db.session.add(Analysis(category_id=category_1.id, name='Analysis #1'))
        db.session.add(Analysis(category_id=category_1.id, name='Analysis #2'))
        db.session.add(Analysis(category_id=category_2.id, name='Analysis #3'))
        db.session.add(Analysis(category_id=category_2.id, name='Analysis #4'))
        db.session.add(Analysis(category_id=category_3.id, name='Analysis #5'))
        db.session.add(Analysis(category_id=category_3.id, name='Analysis #6'))
        db.session.commit()

    if db.session.query(User).count() == 0:
        db.session.add(
            User(
                username='doctor_1',
                password=generate_password_hash('doc_1'),
                public_id=str(uuid.uuid4()),
                is_doctor=True,
            )
        )
        db.session.add(
            User(
                username='doctor_2',
                password=generate_password_hash('doc_2'),
                public_id=str(uuid.uuid4()),
                is_doctor=True,
            )
        )
        db.session.add(
            User(
                username='doctor_3',
                password=generate_password_hash('doc_3'),
                public_id=str(uuid.uuid4()),
                is_doctor=True,
            )
        )
        db.session.add(
            User(
                username='tech_1',
                password=generate_password_hash('tech_1'),
                public_id=str(uuid.uuid4()),
                is_technician=True,
            )
        )
        db.session.add(
            User(
                username='tech_2',
                password=generate_password_hash('tech_2'),
                public_id=str(uuid.uuid4()),
                is_technician=True,
            )
        )
        db.session.add(
            User(
                username='tech_3',
                password=generate_password_hash('tech_3'),
                public_id=str(uuid.uuid4()),
                is_technician=True,
            )
        )

        db.session.commit()


if __name__ == "__main__":
    cli()
