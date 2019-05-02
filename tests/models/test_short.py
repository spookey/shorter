from datetime import datetime

from pytest import mark, raises
from sqlalchemy.exc import IntegrityError

from shorter.models.short import Short
from shorter.start.environment import SYM_POOL

LEN = 6


@mark.usefixtures('session')
class TestShort:

    @staticmethod
    def test_default_fields():
        start = datetime.utcnow()
        short = Short.create(symbol='abc', target='def')

        assert short.prime == 1
        assert short.symbol == 'abc'
        assert short.target == 'def'
        assert short.active is True
        assert start <= short.created
        assert short.created <= datetime.utcnow()
        assert short.visited == 0

    @staticmethod
    def test_symbol_unique():
        one = Short.create(symbol='sym', target='one', _commit=False)
        assert one.save(_commit=True)

        two = Short.create(symbol='sym', target='two', _commit=False)
        with raises(IntegrityError):
            assert two.save(_commit=True)

    @staticmethod
    def test_nullables(session):
        short = Short.create(_commit=False)

        assert short.prime is None
        assert short.symbol is None
        assert short.target is None
        assert short.active is None
        assert short.created is None
        assert short.visited is None

        with raises(IntegrityError):
            short.save(_commit=True)
        session.rollback()

        short.update(symbol='sym', _commit=False)

        with raises(IntegrityError):
            short.save(_commit=True)
        session.rollback()

        short.update(target='tgt', _commit=False)

        short.save(_commit=True)

        assert short.prime == 1
        assert short.symbol == 'sym'
        assert short.target == 'tgt'
        assert short.active is True
        assert short.created is not None
        assert short.visited == 0

    @staticmethod
    def test_present_symbol():
        Short.create(symbol='one', target='1')
        Short.create(symbol='two', target='2')

        assert Short.present_symbol('null') is False
        assert Short.present_symbol('one') is True
        assert Short.present_symbol('two') is True
        assert Short.present_symbol('three') is False

    @staticmethod
    def test_by_symbol():
        one = Short.create(symbol='one', target='1')
        two = Short.create(symbol='two', target='2')

        assert Short.by_symbol('null') is None
        assert Short.by_symbol('one') == one
        assert Short.by_symbol('two') == two
        assert Short.by_symbol('three') is None

    @staticmethod
    def test_by_symbol_active():
        act = Short.create(symbol='act', target='act', active=True)
        ina = Short.create(symbol='ina', target='ina', active=False)

        assert Short.by_symbol_active('lol') is None
        assert Short.by_symbol_active('act') == act
        assert Short.by_symbol_active('ina') is None
        assert Short.by_symbol('ina') == ina

    @staticmethod
    def test_generate_symbol_basic():
        one = Short.generate_symbol(LEN)
        two = Short.generate_symbol(LEN)

        assert one
        assert two
        assert one != two

        assert one != Short.generate_symbol(LEN)
        assert two != Short.generate_symbol(LEN)

    @staticmethod
    def test_generate_symbol_length():
        for num in range(1, 1 + 23):
            sym = Short.generate_symbol(length=num)
            assert sym
            assert len(sym) == num

        assert Short.generate_symbol(length=0) == ''
        assert len(Short.generate_symbol(length=-1)) == 1
        assert len(Short.generate_symbol(length=-2)) == 2

    @staticmethod
    def test_len_symbol_empty():
        assert Short.len_symbol(1) == 1
        assert Short.len_symbol(2) == 2

        assert Short.len_symbol(1) == 1

        assert Short.len_symbol(-2) == 2
        assert Short.len_symbol(-1) == 1

    @staticmethod
    def test_len_symbol():
        assert Short.len_symbol(1) == 1

        for sym in SYM_POOL:
            Short.create(symbol=sym, target=sym, _commit=False)

        assert Short.len_symbol(0) == 2
        assert Short.len_symbol(1) == 2
        assert Short.len_symbol(2) == 2
        assert Short.len_symbol(3) == 3

    @staticmethod
    @mark.slow
    def test_len_symbol_fact():
        assert Short.len_symbol(1) == 1

        for a_sym in SYM_POOL:
            for b_sym in SYM_POOL:
                sym = a_sym + b_sym
                Short.create(symbol=sym, target=sym, _commit=False)
            Short.create(symbol=a_sym, target=a_sym, _commit=False)

        assert Short.len_symbol(0) == 3
        assert Short.len_symbol(1) == 3
        assert Short.len_symbol(2) == 3
        assert Short.len_symbol(3) == 3
        assert Short.len_symbol(4) == 4

    @staticmethod
    def test_make_symbol():
        pool, delim, miss = SYM_POOL.partition(SYM_POOL[-2])
        for sym in pool:
            Short.create(symbol=sym, target=sym, _commit=False)

        symbol = Short.make_symbol(1)
        assert symbol in delim + miss
        Short.create(symbol=symbol, target=symbol, _commit=False)

        symbol = Short.make_symbol(1)
        assert symbol in delim + miss
        Short.create(symbol=symbol, target=symbol, _commit=False)

        assert len(Short.make_symbol(1)) == 2