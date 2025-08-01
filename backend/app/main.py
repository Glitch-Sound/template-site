from app.api.auth import router as router_auth
from app.api.company import router as router_company
from app.api.project import router as router_project
from app.api.project_group import router as router_project_group
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

# fmt: off
app.include_router(router_auth,          prefix="/api")
app.include_router(router_company,       prefix="/api")
app.include_router(router_project,       prefix="/api")
app.include_router(router_project_group, prefix="/api")
app.include_router(router_user,          prefix="/api")
# fmt: on
