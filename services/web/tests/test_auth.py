def test_signup(client):
    response = client.post('/signup', data={'username': 'username_1', 'password': 'password_1'})
    assert response.status_code == 201


def test_signup_with_invalid_data(client):
    response = client.post('/signup', data={'username': '', 'password': 'password_1'})
    assert response.status_code == 400
    assert response.text == 'Username and password required'


def test_signup_existing_user(client):
    response = None
    for _ in range(2):
        response = client.post('/signup', data={'username': 'username_1', 'password': 'password_1'})

    assert response.status_code == 202
    assert response.text == 'User `username_1` already exists. Please Log in.'


def test_login(client, user):
    response = client.post('/login', data={'username': user.username, 'password': 'password'})
    assert response.status_code == 201
    assert response.json['token']


def test_login_with_wrong_username(client, user):
    response = client.post('/login', data={'username': 'wrong username', 'password': 'password'})
    assert response.status_code == 403
    assert response.text == 'User does not exist'


def test_login_with_wrong_password(client, user):
    response = client.post('/login', data={'username': user.username, 'password': 'wrong password'})
    assert response.status_code == 403
    assert response.text == 'Wrong password'
