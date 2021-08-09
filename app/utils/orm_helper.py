from typing import Union
from sqlalchemy.orm.session import Session
from database.models.user import UserModel, UserOrm


class OrmHelper:
    @staticmethod
    def create_user(db: Session, user: Union[UserModel, UserOrm]):
        db.add(user.to_orm())
        return db.commit()

    @staticmethod
    def is_user_exist(db: Session, **kwargs):
        q = db.query(UserOrm).filter_by(**kwargs)
        check = db.query(q.exists())
        return check.scalar()

    @staticmethod
    def get_user(db: Session, id: int):
        return db.query(UserOrm).filter_by(id=id).first()
