import datetime

from app.make_request import make_post_request, make_register_request
import sqlalchemy as sa
from fastapi import HTTPException, APIRouter

from app.models import engine

router = APIRouter()

@router.post("/api/login")
async def login(email: str, password: str):
    data = {
        'email': email,
        'password': password,
    }

    auth_response =  make_post_request(data)

    return {
        "message": "Logged in successfully",
        "status": 200,
        "auth_token": auth_response.get('token'),
    }


@router.post("/api/register")
async def register(name: str, email: str, password: str, role_applied: str):
    if not name or not email or not password or not role_applied:
        raise HTTPException(
            status_code=400, detail="name, email, password, role_applied are required"
        )

    payload = {
        "name": name,
        "email": email,
        "password": password,
        "role_applied": role_applied,
    }
    new_user = make_register_request(payload)

    return {
        "success": True,
        "message": "User registered successfully",
        "user": new_user,
    }