from tests.setup_test import client

def test_no_auth_token():
    response = client.get("/user")
    
    assert response.status_code == 401
    assert response.json() == {
        "error": "Invalid authorization header"
    }

def test_bad_auth_token():
    response = client.get("/user", headers={
        "Authorization": "Bearer bad_token"
    })

    assert response.status_code == 401
    assert response.json() == {
        "error": "Invalid token"
    }

def test_user_not_found():
    response = client.get("/user", headers={
        "Authorization": "Bearer nonexistent_user_token"
    })

    assert response.status_code == 404
    assert response.json() == {
        "error": "User not found"
    }

def test_get_user_ok():
    response = client.get("/user", headers={
        "Authorization": "Bearer dummy_user_token"
    })

    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "first_name": "John",
        "last_name": "Doe",
        "email": "dummy.email@test.loc",
        "password": "hash(#dummy_password123)"
    }