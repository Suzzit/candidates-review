import jwt
from fastapi import HTTPException, Request

secret_key = "Secret key"


def encode_payload(payload):
    return jwt.encode(payload, secret_key, algorithm="HS256")


def decode_token(token):
    try:
        return jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def get_current_user(request: Request):
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

    token = authorization.removeprefix("Bearer ").strip()
    return decode_token(token)


def require_roles(*roles):
    def dependency(request: Request):
        current_user = get_current_user(request)
        if current_user.get("role") not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user

    return dependency