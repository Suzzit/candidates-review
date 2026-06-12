import datetime

import sqlalchemy as sa
from fastapi import HTTPException, APIRouter

from app.models import engine
from app.routers.auth.utils import hash_password
from app.routers.auth.jwt_utils import encode_payload
from app.models.users import Users

router = APIRouter()

@router.post("/api/login")
async def login(email: str, password: str):
    hashed_password = hash_password(password)

    query = sa.select(
        Users.id,
        Users.name,
        Users.password,
        Users.email,
        Users.role,
        Users.role_applied,
        Users.status,
    ).where(
        Users.email == email,
    )

    with engine.connect() as connection:
        result = connection.execute(query).fetchone()

    if result is None:
        raise HTTPException(status_code=401, detail="Invalid email")

    if result.password != hashed_password:
        raise HTTPException(status_code=401, detail="Invalid password")

    payload = {
        **result._asdict(),
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }

    del payload["password"]

    return {
        "message": "Logged in successfully",
        "status": 200,
        "auth_token": encode_payload(payload),
    }


@router.post("/api/register")
async def register(name: str, email: str, password: str, role_applied: str):
    if not name or not email or not password or not role_applied:
        raise HTTPException(
            status_code=400, detail="name, email, password, role_applied are required"
        )

    hashed_password = hash_password(password)

    new_user = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "role_applied": role_applied,
        "status": "new",
        "role": "reviewer",
    }

    insert_query = sa.insert(Users).values(**new_user)

    with engine.connect() as connection:
        connection.execute(insert_query)
        connection.commit()

    return {
        "success": True,
        "message": "User registered successfully",
        "user": new_user,
    }