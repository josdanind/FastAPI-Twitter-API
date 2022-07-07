# Python
from typing import Dict

# FatsAPI
from fastapi import HTTPException, status

# ----------
#  DATABASE
# ----------
# SQLAlchemy
from sqlalchemy.orm  import Session
from . import models

# -------
#  UTILS
# -------
def first_pair(dictionary: Dict):
    key= next(iter(dictionary))
    value = dictionary[key]

    return key, value

# --------------
#  BASE QUERIES
# --------------
# --// GET A ROW
def get_row(db: Session, model, **condition):
    key, value = first_pair(condition)

    return db.query(
        eval(f'models.{model}')
    ).filter(
        eval(f'models.{model}.{key}') == value
    ).first()

# --// GET ALL ROWS
def get_all(db: Session, model, skip:int = 0, limit:int = 100):
    db_data = db.query(
        eval(f'models.{model}')
    ).offset(skip).limit(limit).all()

    return db_data

# --// DELETE A ROW
def delete_row(db:Session, model, **condition):
    key, value = first_pair(condition)

    db.query(
        eval(f'models.{model}')
    ).filter(
        eval(f'models.{model}.{key}') == value
    ).delete()
    db.commit()

# --// WRITE IN A ROW
def write_row(db:Session, model, contentModel):
    db_data = eval(f"models.{model}(**{contentModel})")
    db.add(db_data)
    db.commit()
    db.refresh(db_data)

    return db_data

def check_existence(
    db: Session,
    model,
    error_message=None,
    error_if_exist=False,
    **condition
):
    key, value = first_pair(condition)
    db_data = get_row(db, model, **{f'{key}': value})

    if error_if_exist:
        if db_data:
            raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=error_message)
    else:
        if not db_data:
            raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=error_message)
        else:
            return db_data