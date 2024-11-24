from tests.setup_test import client

def test_user_not_found():
    response = client.post("/chats", headers={
        "Authorization": "Bearer nonexistent_user_token"
    })

    assert response.status_code == 404
    assert response.json() == {
        "error": "User not found"
    }

def test_missing_title():
    requestBody = {}

    response = client.post("/chats", data=requestBody, headers={
        "Authorization": "Bearer dummy_user_token"
    })

    assert response.status_code == 400
    assert response.json() == {
        "error": "Title is required"
    }

def test_failed_to_create_chat():
    requestBody = {
        "title": "error",
    }

    response = client.post("/chats", data=requestBody, headers={
        "Authorization": "Bearer dummy_user_token",
    })

    assert response.status_code == 500
    assert response.json() == {
        "error": "Failed to create chat"
    }

def test_create_chat_ok():
    requestBody = {
        "title": "Chat 3",
    }

    response = client.post("/chats", data=requestBody, headers={
        "Authorization": "Bearer dummy_user_token",
    })

    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "title": "Chat 3",
        "user_id": "1"
    }

def test_create_chat_from_prompt_user_not_found():
    response = client.post("/chats/create", headers={
        "Authorization": "Bearer nonexistent_user_token"
    })

    assert response.status_code == 404
    assert response.json() == {
        "error": "User not found"
    }

def test_create_chat_from_prompt_missing_prompt():
    requestBody = {}

    response = client.post("/chats/create", data=requestBody, headers={
        "Authorization": "Bearer dummy_user_token"
    })

    assert response.status_code == 400
    assert response.json() == {
        "error": "Prompt is required"
    }

def test_create_chat_from_prompt_failed_to_create_chat():
    requestBody = {
        "prompt": "simple_query_error",
    }

    response = client.post("/chats/create", data=requestBody, headers={
        "Authorization": "Bearer dummy_user_token",
    })

    assert response.status_code == 500
    assert response.json() == {
        "error": "Failed to create chat"
    }

def test_create_chat_from_prompt_ok():
    requestBody = {
        "prompt": "Chat 4",
    }

    response = client.post("/chats/create", data=requestBody, headers={
        "Authorization": "Bearer dummy_user_token",
    })

    assert response.status_code == 200
    assert response.json() == {
        "chat": {
            "id": "1",
            "title": "dummy_query_response",
            "user_id": "1"
        },
        "message": "dummy_response"
    }