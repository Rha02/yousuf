from tests.setup_test import client

def test_login_ok():
    requestBody = {
        "email": "dummy.user@test.loc",
        "password": "dummy_password"
    }

    response = client.post("/login", data=requestBody)

    assert response.status_code == 200
    assert "Authorization" in response.headers

def test_login_user_not_found():
    requestBody = {
        "email": "error",
        "password": "dummy_password"
    }

    response = client.post("/login", data=requestBody)

    assert response.status_code == 404
    assert response.json() == {
        "error": "User not found"
    }