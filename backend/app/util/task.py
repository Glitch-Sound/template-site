from datetime import datetime
from zoneinfo import ZoneInfo

from app.database import SessionLocal
from sqlalchemy.orm import Session

JST = ZoneInfo("Asia/Tokyo")


def scheduled_tasks() -> None:
    db: Session = SessionLocal()
    try:
        today_str = datetime.now(JST).date().isoformat()
        print("exec: " + today_str)

        _import_number(db)
        _import_larte_checklist(db)

    finally:
        db.close()


def _import_number(db: Session) -> None:
    pass


def _import_larte_checklist(db: Session) -> None:
    pass
