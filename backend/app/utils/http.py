import json
from fastapi import Response, Request

def jsonResponse(data: dict, status: int = 200) -> Response:
    return Response(
        content=json.dumps(data),
        status_code=status,
        headers={
            "Content-Type": "application/json"
        }
    )

def getAuthToken(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return ""
    
    return auth_header.split(" ")[1]

def getIntQueryParam(request: Request, param: str, defaultInt: int) -> int:
    res = request.query_params.get(param)
    if not res:
        return defaultInt
    try:
        res = int(res)
    except ValueError:
        res = defaultInt

    return res

class ErrorResponses:
    INVALID_AUTH_TOKEN = jsonResponse({
        "error": "Invalid authorization header"
    }, 401)
    USER_NOT_FOUND = jsonResponse({
        "error": "User not found"
    }, 404)
    INCORRECT_PASSWORD = jsonResponse({
        "error": "Incorrect password"
    }, 401)
    FORBIDDEN = jsonResponse({
        "error": "Unauthorized"
    }, 403)
    CHAT_NOT_FOUND = jsonResponse({
        "error": "Chat not found"
    }, 404)