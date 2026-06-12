from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.routers.auth as auth_router
import app.routers.candidates as candidate_router

app = FastAPI()
app.include_router(auth_router.router)
app.include_router(candidate_router.router)
