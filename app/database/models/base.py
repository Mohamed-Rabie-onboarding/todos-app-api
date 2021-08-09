from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class IToOrm:
    def to_orm(self):
        return self
