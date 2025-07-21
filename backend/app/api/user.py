from app.database import get_db
from app.schemas import user as schema_user
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/users", response_model=list[schema_user.User])
def get_users(db: Session = Depends(get_db)):
    return ""
