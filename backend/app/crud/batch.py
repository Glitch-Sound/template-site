import csv
import glob
import io
from datetime import date

from app.models import project as model_project
from app.models import project_number as model_project_number
from sqlalchemy import and_
from sqlalchemy.orm import Session


def import_number(db: Session) -> None:
    csv_paths = glob.glob("/app/import/daicholist_*.csv")
    if not csv_paths:
        return

    today_str = date.today().isoformat()
    # fmt: off
    targets = db.query(
        model_project.Project.rid,
        model_project.Project.number_parent,
    )\
    .filter(
        and_(
            model_project.Project.number_parent.isnot(None),
            model_project.Project.number_parent != "",
            model_project.Project.date_end >= today_str,
            model_project.Project.is_deleted == 0,
        )
    )\
    .all()
    # fmt: on

    if not targets:
        return

    prefix_map = {}
    dict_parent_rids = {}
    for rid, number_parent in targets:
        prefix = (number_parent or "")[:4]
        if not prefix:
            continue
        prefix_map.setdefault(prefix, set()).add(number_parent)
        dict_parent_rids.setdefault(number_parent, []).append(rid)

    csv_path = csv_paths[0]
    with open(csv_path, "rb") as file:
        raw_bytes = file.read()
    try:
        text = raw_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw_bytes.decode("cp932")

    reader = csv.reader(io.StringIO(text))
    next(reader, None)

    dict_number = {}
    for row in reader:
        if len(row) <= 16:
            continue
        number = row[2].strip()
        if not number:
            continue
        prefix = number[:4]
        if prefix not in prefix_map:
            continue
        info = (number, row[3].strip(), row[15].strip(), row[16].strip())
        for number_parent in prefix_map[prefix]:
            dict_number.setdefault(number_parent, []).append(info)

    for number_parent, items in dict_number.items():
        rid_projects_list = dict_parent_rids.get(number_parent)
        if not rid_projects_list:
            continue
        has_m = any(len(number) >= 5 and number[4] == "M" for number, _, _, _ in items)
        has_s = any(len(number) >= 5 and number[4] == "S" for number, _, _, _ in items)
        has_o = any(len(number) >= 5 and number[4] == "0" for number, _, _, _ in items)
        for rid_projects in rid_projects_list:
            db.query(model_project.Project).filter(
                model_project.Project.rid == rid_projects
            ).update(
                {
                    "number_m": 1 if has_m else 0,
                    "number_s": 1 if has_s else 0,
                    "number_o": 1 if has_o else 0,
                },
                synchronize_session=False,
            )
            db.query(model_project_number.ProjectNumber).filter(
                model_project_number.ProjectNumber.rid_projects == rid_projects
            ).delete(synchronize_session=False)

            for number, note, date_start, date_end in items:
                type_number = model_project_number.TypeNumber.NONE.value
                if len(number) >= 5:
                    fifth = number[4]
                    if fifth == "M":
                        type_number = model_project_number.TypeNumber.M.value
                    elif fifth == "S":
                        type_number = model_project_number.TypeNumber.S.value
                    elif fifth == "0":
                        type_number = model_project_number.TypeNumber.O.value
                obj_number = model_project_number.ProjectNumber(
                    rid_projects=rid_projects,
                    type=type_number,
                    number=number,
                    note=note,
                    date_start=date_start,
                    date_end=date_end,
                )
                db.add(obj_number)

    db.commit()


def import_larte_checklist(db: Session) -> None:
    pass
