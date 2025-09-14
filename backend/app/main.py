from contextlib import asynccontextmanager

from app.api.auth import router as router_auth
from app.api.company import router as router_company
from app.api.project import router as router_project
from app.api.summary import router as router_summary
from app.api.thread import router as router_thread
from app.api.user import router as router_user
from app.database import Base, engine
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from pytz import timezone
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

JST = timezone("Asia/Tokyo")
scheduler = BackgroundScheduler(
    timezone=JST,
    job_defaults={
        "coalesce": True,
        "misfire_grace_time": 3600,
        "max_instances": 1,
    },
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    trigger = CronTrigger(hour=0, minute=0, second=0, timezone=JST)
    scheduler.add_job(
        app.api.summary.scheduled_summaries,
        trigger,
        id="daily_summary_job",
        replace_existing=True,
    )
    scheduler.start()
    try:
        yield
    finally:
        scheduler.shutdown(wait=False)


# fmt: off
app.include_router(router_auth,    prefix="/api")
app.include_router(router_company, prefix="/api")
app.include_router(router_project, prefix="/api")
app.include_router(router_summary, prefix="/api")
app.include_router(router_thread,  prefix="/api")
app.include_router(router_user,    prefix="/api")
# fmt: on
