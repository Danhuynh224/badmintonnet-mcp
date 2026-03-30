from contextvars import ContextVar

_request_headers: ContextVar[dict | None] = ContextVar(
    "request_headers",
    default=None
)

def set_request_headers(headers: dict | None):
    _request_headers.set(headers)

def get_access_token():
    headers = _request_headers.get()

    if not headers:
        return None

    auth = headers.get("authorization") or headers.get("Authorization")

    if not auth:
        return None

    if auth.startswith("Bearer "):
        return auth.replace("Bearer ", "")

    return auth