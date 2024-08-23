import json
from fastapi import Response

def jsonResponse(data: dict, status: int = 200) -> Response:
    return Response(
        content=json.dumps(data),
        status_code=status,
        headers={
            "Content-Type": "application/json"
        }
    )