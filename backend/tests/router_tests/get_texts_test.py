from tests.setup_test import client

def test_chat_not_found():
    response = client.get("/chats/error/uploaded_texts", headers={
        "Authorization": "Bearer dummy_user_token"
    })

    assert response.status_code == 404
    assert response.json() == {
        "error": "Chat not found"
    }

def test_user_unauthorized():
    response = client.get("/chats/1/uploaded_texts", headers={
        "Authorization": "Bearer dummy_other_user_token"
    })

    assert response.status_code == 403
    assert response.json() == {
        "error": "Unauthorized"
    }

def test_get_texts_ok():
    response = client.get("/chats/1/uploaded_texts", headers={
        "Authorization": "Bearer dummy_user_token"
    })

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "1",
            "chat_id": "1",
            "file_name": "file1.txt",
            "file_size": 100,
            "file_type": "text/plain",
            "uploaded_at": "2021-01-01 12:00:00"
        },
        {
            "id": "2",
            "chat_id": "1",
            "file_name": "file2.txt",
            "file_size": 200,
            "file_type": "text/plain",
            "uploaded_at": "2021-01-01 12:00:00"
        }
    ]