from pytest import fixture, mark

from shorter.database import CRUDMixin
from shorter.start.extensions import DB

# pylint: disable=no-member

PAYLOAD = "omg wtf bbq"
LAYPOAD = "napfkuchen!"


class CRUDMixinPhony(CRUDMixin, DB.Model):
    prime = DB.Column(DB.Integer(), primary_key=True)
    value = DB.Column(DB.String())


@fixture(scope="function")
def _crud_c():
    return CRUDMixinPhony.create(value=PAYLOAD, _commit=True)


@fixture(scope="function")
def _crud_nc():
    return CRUDMixinPhony.create(value=PAYLOAD, _commit=False)


@mark.usefixtures("session")
class TestCRUDMixin:
    @staticmethod
    def test_create_no_commit(_crud_nc):
        assert _crud_nc.prime is None
        assert _crud_nc.value == PAYLOAD
        assert _crud_nc in CRUDMixinPhony.query.all()

    @staticmethod
    def test_create_commit(_crud_c):
        assert _crud_c.prime == 1
        assert _crud_c.value == PAYLOAD
        assert _crud_c in CRUDMixinPhony.query.all()

    @staticmethod
    def test_update_no_comit(_crud_nc):
        assert _crud_nc.value == PAYLOAD
        _crud_nc.update(value=LAYPOAD, _commit=False)
        assert _crud_nc.value == LAYPOAD

    @staticmethod
    def test_update_comit(_crud_c):
        assert _crud_c.value == PAYLOAD
        _crud_c.update(value=LAYPOAD, _commit=True)
        assert _crud_c.value == LAYPOAD

    @staticmethod
    def test_save_no_commit(session, _crud_nc):
        assert _crud_nc not in session.dirty
        _crud_nc.value = LAYPOAD
        assert _crud_nc not in session.dirty
        _crud_nc.save(_commit=False)
        assert _crud_nc not in session.dirty

    @staticmethod
    def test_save_commit(session, _crud_c):
        assert _crud_c not in session.dirty
        _crud_c.value = LAYPOAD
        assert _crud_c in session.dirty
        _crud_c.save(_commit=True)
        assert _crud_c not in session.dirty

    @staticmethod
    def test_delete_no_commit(_crud_nc):
        assert _crud_nc in CRUDMixinPhony.query.all()
        _crud_nc.delete(_commit=False)
        assert _crud_nc not in CRUDMixinPhony.query.all()

    @staticmethod
    def test_delete_commit(_crud_c):
        assert _crud_c in CRUDMixinPhony.query.all()
        _crud_c.delete(_commit=True)
        assert _crud_c not in CRUDMixinPhony.query.all()
