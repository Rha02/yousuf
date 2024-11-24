from tests.setup_test import client

def test_chat_not_found():
    response = client.get("/chats/error", headers={
        "Authorization": "Bearer dummy_user_token"
    })

    assert response.status_code == 404
    assert response.json() == {
        "error": "Chat not found"
    }

def test_user_unauthorized():
    response = client.get("/chats/1", headers={
        "Authorization": "Bearer dummy_other_user_token"
    })

    assert response.status_code == 403
    assert response.json() == {
        "error": "Unauthorized"
    }

def test_get_messages_ok():
    response = client.get("/chats/1", headers={
        "Authorization": "Bearer dummy_user_token"
    })

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "1",
            "session_id": "1",
            "history": {
                "type": "Human",
                "data": {
                    "content": "Human message"
                }
            }
        },
        {
            "id": "2",
            "session_id": "1",
            "history": {
                "type": "Bot",
                "data": {
                    "content": "Bot message"
                }
            }
        }
    ]