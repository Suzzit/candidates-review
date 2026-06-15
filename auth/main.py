from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import sqlalchemy as sa
from models.users import Users
from models import engine
from utils import hash_password

from jwt_utils import create_token


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://localhost:\d+",
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/v1/auth/login')
async def login(request: Request):
    data = await request.json()
    hashed_password = hash_password(data.get('password'))

    query = sa.select(
        Users.id,
        Users.fullname,
        Users.password,
        Users.email,
        Users.role,
        Users.role_applied,
        Users.status,
    ).where(
        Users.email == data.get('email'),
    )

    with engine.connect() as connection:
        result = connection.execute(query).fetchone()

    if result is None:
        raise HTTPException(status_code=401, detail="Invalid email")

    if result.password != hashed_password:
        raise HTTPException(status_code=401, detail="Invalid password")

    payload = {
        **result._asdict(),
    }

    del payload["password"]

    token = create_token(payload)

    return {"message": "jwt token", 'token': token}


@app.post('/v1/auth/register')
async def register(request: Request):
    data = await request.json()
    hashed_password = hash_password(data.get('password'))

    new_user = {
        "fullname": data.get('name'),
        "email": data.get('email'),
        "password": hashed_password,
        "role_applied": data.get('role_applied'),
        "status": "new",
        "role": "reviewer",
    }

    insert_query = sa.insert(Users).values(**new_user)

    with engine.connect() as connection:
        connection.execute(insert_query)
        connection.commit()

    return new_user


@app.get("/v1/auth/public-key")
async def get_public_key():
    with open("public.pem", "r") as f:
        return {"public_key": f.read()}
