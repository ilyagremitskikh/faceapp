from abc import ABC, abstractmethod
from typing import Iterable

from sqlalchemy import any_
from sqlalchemy.orm import Session

from app.models import Base
from app.models.models import PornstarOrm


class DbRepository(ABC):
    @abstractmethod
    def get_by_ids(self, model: Base, ids: Iterable[int], session: Session):
        pass

    @abstractmethod
    def get_all(self, model: Base, session: Session):
        pass


class PornstarRepository(DbRepository):
    def get_all(self, session: Session, model: Base = PornstarOrm):
        with session.begin() as sess:
            results = sess.query(PornstarOrm).all()
        return results

    def get_by_ids(self, ids: Iterable[int], session: Session, model: Base = PornstarOrm):
        with session.begin() as sess:
            results = sess.query(PornstarOrm).filter(PornstarOrm.id == (any_(ids)))
        return results
