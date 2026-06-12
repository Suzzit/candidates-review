from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.routers.auth as auth_router
import app.routers.candidates as candidate_router

app = FastAPI()
app.include_router(auth_router.router)
app.include_router(candidate_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://localhost:\d+",
    allow_methods=["*"],
    allow_headers=["*"],
)

