from app.make_request import get_public_key
import jwt
from fastapi import HTTPException, Request


def decode_token(token):
    public_key = get_public_key().get('public_key')
    print('\n' * 5, public_key)
    try:
        return jwt.decode(token, public_key, algorithms=["RS256"])
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