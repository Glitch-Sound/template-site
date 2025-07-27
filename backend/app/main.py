from app.api.auth import router as router_auth
from app.api.user import router as router_user
from app.database import Base, engine
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_auth, prefix="/api")
app.include_router(router_user, prefix="/api")
