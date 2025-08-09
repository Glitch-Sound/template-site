from app.api import common as api_common
from app.crud import company as crud_company
from app.database import get_db
from app.schemas import company as schema_company
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(tags=["Company"])


@router.get("/companies", response_model=list[schema_company.Company])
def get_companies(
    db: Session = Depends(get_db), _current_user=Depends(api_common.log_token_user)
):
    try:
        return crud_company.get_companies(db)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/companies", response_model=schema_company.Company)
def create_company(
    target: schema_company.CompanyCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        result = crud_company.create_company(db, target)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.put("/companies", response_model=schema_company.Company)
def update_company(
    target: schema_company.CompanyUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        result = crud_company.update_company(db, target)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/companies/{rid}", response_model=None)
def delete_company(
    rid: int,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        crud_company.delete_company(db, rid)
        return {"result": "deleted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
