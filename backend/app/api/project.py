from app.api import common as api_common
from app.crud import project as crud_project
from app.database import get_db
from app.schemas import project as schema_project
from app.schemas import user as schema_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(tags=["Project"])


@router.get("/project_groups", response_model=list[schema_project.ProjectGroup])
def get_project_groups(
    db: Session = Depends(get_db), _current_user=Depends(api_common.log_token_user)
):
    try:
        return crud_project.get_project_groups(db)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/project_groups", response_model=schema_project.ProjectGroup)
def create_project_group(
    target: schema_project.ProjectGroupCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        result = crud_project.create_project_group(db, target)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.put("/project_groups", response_model=schema_project.ProjectGroup)
def update_project_group(
    target: schema_project.ProjectGroupUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        result = crud_project.update_project_group(db, target)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/project_groups/{rid}", response_model=None)
def delete_project_group(
    rid: int,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        crud_project.delete_project_group(db, rid)
        return {"result": "deleted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/projects/condition", response_model=schema_project.SearchCondition)
def get_project_condition(
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_project.get_project_condition(db)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/projects/targets", response_model=list[schema_project.TargetQuarter])
def get_project_targets(
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_project.get_project_targets(db)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/projects/users", response_model=list[schema_user.User])
def get_project_users(
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_project.get_project_users(db)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/projects/search", response_model=list[schema_project.ProjectList])
def get_projects(
    condition: schema_project.SearchCondition,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_project.get_projects(db, condition)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/projects", response_model=schema_project.Project)
def create_project(
    target: schema_project.ProjectCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        result = crud_project.create_project(db, target)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.put("/projects", response_model=schema_project.Project)
def update_project(
    target: schema_project.ProjectUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        result = crud_project.update_project(db, target)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/projects/{rid}", response_model=None)
def delete_project(
    rid: int,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        crud_project.delete_project(db, rid)
        return {"result": "deleted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
