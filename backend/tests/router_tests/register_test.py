from tests.setup_test import client

def test_register_invalid_email():
    requestBody = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "error",
        "password": "#dummy_password123"
    }

    response = client.post("/register", data=requestBody)

    assert response.status_code == 400
    assert response.json() == {
        "error": "Invalid email"
    }

def test_register_invalid_password():
    requestBody = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "dummy.user@test.loc",
        "password": "123"
    }

    response = client.post("/register", data=requestBody)

    assert response.status_code == 400
    assert response.json() == {
        "error": "Invalid password"
    }

def test_register_invalid_first_name():
    requestBody = {
        "first_name": "12",
        "last_name": "Doe",
        "email": "dummy.user@test.loc",
        "password": "#dummy_password123"
    }

    response = client.post("/register", data=requestBody)

    assert response.status_code == 400
    assert response.json() == {
        "error": "Invalid first name"
    }

def test_register_invalid_last_name():
    requestBody = {
        "first_name": "John",
        "last_name": "D",
        "email": "dummy.user@test.loc",
        "password": "#dummy_password123"
    }

    response = client.post("/register", data=requestBody)

    assert response.status_code == 400
    assert response.json() == {
        "error": "Invalid last name"
    }

def test_register_hash_error():
    requestBody = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "dummy.user@test.loc",
        "password": "BadPassword1!"
    }

    response = client.post("/register", data=requestBody)

    assert response.status_code == 500
    assert response.json() == {
        "error": "Hashing failed"
    }  

# create user?
def test_register_create_user_error():
    requestBody = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "CreateUserError@test.loc",
        "password": "#dummy_password123"
    }

    response = client.post("/register", data=requestBody)

    assert response.status_code == 500
    assert response.json() == {
        "error": "Creating error failed"
    }  

def test_register_ok():
    requestBody = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "dummy.user@test.loc",
        "password": "#dummy_password123"
    }

    response = client.post("/register", data=requestBody)

    assert response.status_code == 201
    assert "Authorization" in response.headers