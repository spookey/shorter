from pytest import fixture, mark

from shorter.database import PrimeMixin
from shorter.start.extensions import DB

# pylint: disable=no-member
# pylint: disable=too-few-public-methods


class PrimeMixinPhony(PrimeMixin, DB.Model):
    pass


@fixture
def _pri():
    return PrimeMixinPhony()


@mark.usefixtures('session')
class TestPrimeMixin:

    @staticmethod
    def test_tablename(_pri):
        assert _pri.__tablename__ == 'primemixinphony'

    @staticmethod
    def test_primekey_init(_pri):
        assert _pri is not None
        assert _pri.prime is None

    @staticmethod
    def test_primekey_autoset(session):
        one = PrimeMixinPhony()
        two = PrimeMixinPhony()
        session.add_all((one, two))
        session.commit()
        assert one.prime == 1
        assert two.prime == 2

    @staticmethod
    def test_by_prime_not_found():
        res = PrimeMixinPhony.by_prime(1337)
        assert res is None

    @staticmethod
    def test_by_prime(session, _pri):
        session.add(_pri)
        session.commit()
        assert _pri == PrimeMixinPhony.by_prime(1)

    @staticmethod
    def test_by_prime_types(session, _pri):
        session.add(_pri)
        session.commit()
        assert _pri == PrimeMixinPhony.by_prime(1)
        assert _pri == PrimeMixinPhony.by_prime(1.0)
        assert _pri == PrimeMixinPhony.by_prime('1')
        assert _pri == PrimeMixinPhony.by_prime(b'1')

    @staticmethod
    def test_by_prime_invalid(session, _pri):
        session.add(_pri)
        session.commit()
        assert _pri == PrimeMixinPhony.by_prime(1)
        assert None is PrimeMixinPhony.by_prime(-1)
        assert None is PrimeMixinPhony.by_prime(0.1)
        assert None is PrimeMixinPhony.by_prime('omg')
        assert None is PrimeMixinPhony.by_prime(b'wtf')
