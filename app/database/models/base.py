from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class IToOrm:
    """ class IToOrm
        provide a default implementation for to_orm method
    """

    def to_orm(self):
        return self
