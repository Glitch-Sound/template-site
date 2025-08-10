from app.api.auth import router as router_auth
from app.api.company import router as router_company
from app.api.project import router as router_project
from app.api.thread import router as router_thread
from app.api.user import router as router_user
from app.database import Base, engine
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "Accept",
        "X-Requested-With",
    ],
)

# fmt: off
app.include_router(router_auth,    prefix="/api")
app.include_router(router_company, prefix="/api")
app.include_router(router_project, prefix="/api")
app.include_router(router_user,    prefix="/api")
app.include_router(router_thread,  prefix="/api")
# fmt: on
