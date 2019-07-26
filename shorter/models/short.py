from datetime import datetime
from random import choice

from sqlalchemy import and_

from shorter.database import Model
from shorter.start.environment import DELAY_DEF, SYM_MINI, SYM_POOL
from shorter.start.extensions import DB
from shorter.start.helper import parse_int

# pylint: disable=no-member


class Short(Model):
    symbol = DB.Column(DB.String(length=256), unique=True, nullable=False)
    target = DB.Column(DB.String(length=1024), nullable=False)
    delay = DB.Column(DB.Integer(), nullable=False, default=DELAY_DEF)
    active = DB.Column(DB.Boolean(), nullable=False, default=True)
    visited = DB.Column(DB.Integer(), nullable=False, default=0)
    created = DB.Column(DB.DateTime(), nullable=False, default=datetime.utcnow)

    @classmethod
    def by_symbol(cls, symb):
        return cls.query.filter(cls.symbol == symb).first()

    @classmethod
    def by_symbol_active(cls, symb):
        result = cls.by_symbol(symb)
        if not result:
            return None
        if not result.active:
            return None
        return result

    @staticmethod
    def generate_symbol(length):
        return ''.join(choice(SYM_POOL) for _ in range(1, 1 + abs(length)))

    @classmethod
    def len_symbol(cls, minimum=SYM_MINI):
        result = abs(minimum if minimum != 0 else 1)
        count = cls.query.count()
        size = len(SYM_POOL)
        while pow(size, result) <= count:
            result += 1
        return result

    @classmethod
    def make_symbol(cls, minimum=SYM_MINI):
        length = cls.len_symbol(minimum=minimum)
        result = cls.generate_symbol(length)
        while cls.by_symbol(result) is not None:
            result = cls.generate_symbol(length)
        return result

    @classmethod
    def generate(cls, target, delay=DELAY_DEF, _commit=True, **kwargs):
        short = cls.query.filter(and_(
            cls.target == target,
            cls.delay == delay,
            cls.active.is_(True),
        )).first()
        if short is not None:
            return short

        return cls.create(
            symbol=cls.make_symbol(minimum=SYM_MINI),
            target=target,
            delay=delay,
            _commit=_commit,
            **kwargs
        )

    def increase_visit(self, _commit=True):
        value = parse_int(self.visited)
        return self.update(visited=1 + value, _commit=_commit)

    @classmethod
    def ordered(cls, field, rev=False):
        field = field if field is not None else 'prime'

        coll = cls.__table__.columns.get(field, None)
        if coll is None:
            return None

        return cls.query.order_by(coll.desc() if rev else coll.asc())
