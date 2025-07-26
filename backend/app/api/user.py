from app.crud import user as crud_user
from app.database import get_db
from app.schemas import user as schema_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(tags=["User"])


@router.get("/user", response_model=list[schema_user.User])
def get_users(db: Session = Depends(get_db)):
    try:
        return crud_user.get_users(db)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/user", response_model=schema_user.User)
def create_user(target: schema_user.UserCreate, db: Session = Depends(get_db)):
    try:
        result = crud_user.create_user(db, target)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.put("/user", response_model=schema_user.User)
def update_user(target: schema_user.UserUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_user.update_user(db, target)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/user/{rid}", response_model=None)
def delete_user(rid: int, db: Session = Depends(get_db)):
    try:
        crud_user.delete_user(db, rid)
        return {"result": "deleted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
