from re import IGNORECASE
from re import compile as re_compile

from pytest import raises
from wtforms.validators import ValidationError

from shorter.forms.short import check_blocked

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

def _make_list(*entries):
    return [re_compile(line, IGNORECASE) for line in entries]


def test_block_empty():

    for value in [fl for at in [ALLOWED, BLOCKED] for fl in at]:
        assert check_blocked(value, []) is None, value


def test_block_matches():
    for value in ALLOWED:
        assert check_blocked(value, RULES) is None, value

    for value in BLOCKED:
        with raises(ValidationError):
            assert check_blocked(value, RULES), value
