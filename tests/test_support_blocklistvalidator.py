from collections import namedtuple
from re import IGNORECASE
from re import compile as re_compile

from pytest import raises
from wtforms.validators import ValidationError

from shorter.support import BlocklistValidator

RULES = [re_compile(line, IGNORECASE) for line in (
    r'^.+example\.com$',
    r'^http:.+',
    r'.+what\/ever',
    r'.+\d{4,}',
)]
ALLOWED = (
    'https://www.example.org',
    'https://www.example.com/',
    'https://www.example.org/whatever',
    'https://www.example.org/123',
)
BLOCKED = (
    'http://www.example.org',
    'https://www.example.com',
    'https://www.example.org/what/ever',
    'https://www.example.org/12345',
)


def test_is_blocked_empty():
    validator = BlocklistValidator([])

    for value in [fl for at in [ALLOWED, BLOCKED] for fl in at]:
        assert validator.is_blocked(value) is False, value


def test_is_blocked_matches():
    validator = BlocklistValidator(RULES)
    for value in ALLOWED:
        assert validator.is_blocked(value) is False, value

    for value in BLOCKED:
        assert validator.is_blocked(value) is True, value


def test_is_blocked_raises():
    validator = BlocklistValidator(RULES)
    fakefield = namedtuple('FakeField', ('data'))

    for value in ALLOWED:
        assert validator(None, fakefield(value)) is None

    for value in BLOCKED:
        with raises(ValidationError) as verr:
            assert validator(None, fakefield(value)) is None
            assert 'not possible' in verr.message.lower()
