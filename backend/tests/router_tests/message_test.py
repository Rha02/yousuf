from tests.setup_test import client

def test_chat_not_found():
    response = client.post("/chats/error/message", headers={
        "Authorization": "Bearer dummy_user_token"
    })

    assert response.status_code == 404
    assert response.json() == {
        "error": "Chat not found"
    }

def test_user_unauthorized():
    response = client.post("/chats/1/message", headers={
        "Authorization": "Bearer dummy_other_user_token"
    })

    assert response.status_code == 403
    assert response.json() == {
        "error": "Unauthorized"
    }

def test_missing_prompt():
    requestBody = {}

    response = client.post("/chats/1/message", data=requestBody, headers={
        "Authorization": "Bearer dummy_user_token"
    })

    assert response.status_code == 400
    assert response.json() == {
        "error": "Prompt is required"
    }

def test_message_ok():
    requestBody = {
        "prompt": "Hello"
    }

    response = client.post("/chats/1/message", data=requestBody, headers={
        "Authorization": "Bearer dummy_user_token"
    })

    assert response.status_code == 200
    assert response.json() == {
        "message": "dummy_response"
    }