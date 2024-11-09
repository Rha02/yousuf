from tests.setup_test import client

def test_logout_ok():
    response = client.post("/logout")
    
    assert response.status_code == 200
    assert response.json() == {
        "message": "Logout"
    }