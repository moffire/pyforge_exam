from project.models import db, Analysis, Category, DoctorOrder, Order, User


def test_get_analyzes_list(client, patient_token):
    db.session.add(Category(name='Category #1'))
    db.session.commit()

    category = Category.query.filter_by(name='Category #1').first()

    db.session.add(Analysis(category_id=category.id, name='Analysis #1'))
    db.session.add(Analysis(category_id=category.id, name='Analysis #2'))
    db.session.commit()

    analysis_1 = Analysis.query.filter_by(name='Analysis #1').first()
    analysis_2 = Analysis.query.filter_by(name='Analysis #2').first()

    response = client.get('/analyses', headers={'x-access-tokens': f'{patient_token}'})
    assert response.json == [
        {
            'analyzes': [
                {'id': analysis_1.id, 'name': analysis_1.name},
                {'id': analysis_2.id, 'name': analysis_2.name},
            ],
            'id': category.id,
            'name': category.name,
        }
    ]


def test_create_analyses(client, patient_token, doctor):
    db.session.add(Category(name='Category #1'))
    db.session.commit()
    category = Category.query.filter_by(name='Category #1').first()

    db.session.add(Analysis(category_id=category.id, name='Analysis #1'))
    db.session.commit()

    analysis = Analysis.query.filter_by(name='Analysis #1').first()

    response = client.post(
        '/analyses',
        headers={'x-access-tokens': f'{patient_token}'},
        data={'analysis_id': analysis.id, 'doctors_ids': [doctor.id]},
    )
    assert response.status_code == 201
    assert Order.query.count() == 1
