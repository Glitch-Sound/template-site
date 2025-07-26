from app.api.auth import router as router_auth
from app.api.user import router as router_user
from app.database import Base, engine
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(router_auth)
app.include_router(router_user)
