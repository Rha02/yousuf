from tests.setup_test import client

def test_get_chats_ok():
    response = client.get("/chats", headers={
        "Authorization": "Bearer dummy_user_token"
    })

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "1",
            "title": "Chat 1",
            "user_id": "1"
        },
        {
            "id": "2",
            "title": "Chat 2",
            "user_id": "1"
        }
    ]