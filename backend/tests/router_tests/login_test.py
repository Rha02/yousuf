from tests.setup_test import client

def test_login_invalid_email():
    requestBody = {
        "email": "error",
        "password": "#dummy_password123"
    }

    response = client.post("/login", data=requestBody)

    assert response.status_code == 400
    assert response.json() == {
        "error": "Invalid email"
    }

def test_login_ok():
    requestBody = {
        "email": "dummy.user@test.loc",
        "password": "#dummy_password123"
    }

    response = client.post("/login", data=requestBody)

    assert response.status_code == 200
    assert "Authorization" in response.headers

def test_login_user_not_found():
    requestBody = {
        "email": "notfound@test.com",
        "password": "#dummy_password123"
    }

    response = client.post("/login", data=requestBody)

    assert response.status_code == 404
    assert response.json() == {
        "error": "User not found"
    }
    
def test_login_wrong_password():
    requestBody = {
        "email": "dummy.user@test.loc",
        "password": "wrongpassword"
    }

    response = client.post("/login", data=requestBody)

    assert response.status_code == 401
    assert response.json() == {
        "error": "Incorrect password"
    }