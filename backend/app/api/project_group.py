from app.api import common as api_common
from app.crud import project_group as crud_project_group
from app.database import get_db
from app.schemas import project_group as schema_project_group
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(tags=["Project Group"])


@router.get("/project_group", response_model=list[schema_project_group.ProjectGroup])
def get_project_groups(
    db: Session = Depends(get_db), _current_user=Depends(api_common.log_token_user)
):
    try:
        return crud_project_group.get_project_groups(db)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/project_group", response_model=schema_project_group.ProjectGroup)
def create_project_group(
    target: schema_project_group.ProjectGroupCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        result = crud_project_group.create_project_group(db, target)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.put("/project_group", response_model=schema_project_group.ProjectGroup)
def update_project_group(
    target: schema_project_group.ProjectGroupUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        result = crud_project_group.update_project_group(db, target)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/project_group/{rid}", response_model=None)
def delete_project_group(
    rid: int,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        crud_project_group.delete_project_group(db, rid)
        return {"result": "deleted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
