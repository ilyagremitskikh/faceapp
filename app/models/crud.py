from typing import Iterable

from sqlalchemy import any_
from sqlalchemy.orm import Session

from . import models


def get_pornstar(db: Session, pornstar_id: int):
    return (
        db.query(models.PornstarOrm)
        .filter(models.PornstarOrm.id == pornstar_id)
        .first()
    )


def get_pornstars_by_ids(db: Session, pornstars_ids: Iterable):
    return (
        db.query()
        .with_entities(models.PornstarOrm.id)
        .filter(models.PornstarOrm.id == any_(pornstars_ids))
        .all()
    )


def get_pornstars(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PornstarOrm).offset(skip).limit(limit).all()


def save_pornstar(db: Session, pornstar: models.PornstarOrm):
    db.add(pornstar)
    db.commit()
