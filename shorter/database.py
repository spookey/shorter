from sqlalchemy.ext.declarative import declared_attr

from shorter.start.extensions import DB

# pylint: disable=no-member


class CRUDMixin:

    @classmethod
    def create(cls, _commit=True, **kwargs):
        inst = cls(**kwargs)
        return inst.save(_commit=_commit)

    def update(self, _commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if _commit:
            return self.save(_commit=_commit)
        return self

    def save(self, _commit=True):
        DB.session.add(self)
        if _commit:
            DB.session.commit()
        return self

    def delete(self, _commit=True):
        DB.session.delete(self)
        if _commit:
            DB.session.commit()
        return True


class PrimeMixin:
    prime = DB.Column(DB.Integer(), primary_key=True)

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    @classmethod
    def by_prime(cls, value):
        if any([
                isinstance(value, (bytes, str)) and value.isdigit(),
                isinstance(value, (float, int))
        ]):
            return cls.query.get(int(value))
        return None


class Model(CRUDMixin, PrimeMixin, DB.Model):
    __abstract__ = True
