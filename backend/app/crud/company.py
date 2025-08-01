from typing import List

from app.models import company as model_company
from app.schemas import company as schema_company
from sqlalchemy.orm import Session


def get_companies(db: Session) -> List[model_company.Company]:
    # fmt: off
    query = db.query(
        model_company.Company
    )\
    .filter(~model_company.Company.is_deleted)\
    .order_by(model_company.Company.rid)
    # fmt: on
    return query.all()


def create_company(
    db: Session, target: schema_company.CompanyCreate
) -> model_company.Company:
    # fmt: off
    obj_company = model_company.Company(
        name=target.name,
        detail=target.detail,
    )
    # fmt: on

    db.add(obj_company)
    db.commit()
    db.refresh(obj_company)
    return obj_company


def update_company(
    db: Session, target: schema_company.CompanyUpdate
) -> model_company.Company:
    # fmt: off
    obj_company = db.query(
        model_company.Company
    )\
    .filter(model_company.Company.rid == target.rid)\
    .first()

    obj_company.name   = target.name
    obj_company.detail = target.detail
    # fmt: on

    db.commit()
    db.refresh(obj_company)
    return obj_company


def delete_company(db: Session, rid: int) -> None:
    # fmt: off
    obj_company = db.query(
        model_company.Company
    )\
    .filter(model_company.Company.rid == rid)\
    .first()
    # fmt: on

    obj_company.is_deleted = True
    db.commit()
