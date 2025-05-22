HTML_RESPONSE = {
    200: {
        "content": {"text/html": {
            "example": "<html><body><h1>Пример HTML</h1></body></html>"
        }},
        "description": "HTML страница",
    }
}

UNAUTHORIZED = {
    401: {
        "description": "Error: Unauthorized",
        "content": {
            "application/json": {
                "example": {"detail": "Not authenticated / Incorrect username or password"}
            }
        }
    }
}

FORBIDDEN = {
    403: {
        "description": "Error: Forbidden",
        "content": {
            "application/json": {
                "example": {"detail": "Invalid or expired token"}
            }
        }
    }
}

NOT_FOUND = {
    404: {
        "description": "Error: Not Found",
        "content": {
            "application/json": {
                "example": {"detail": "Item not found"}
            }
        }
    }
}