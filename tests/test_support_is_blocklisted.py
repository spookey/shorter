from re import IGNORECASE
from re import compile as re_compile

from shorter.support import is_blocklisted

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
        assert is_blocklisted(value, []) is False, value


def test_block_matches():
    for value in ALLOWED:
        assert is_blocklisted(value, RULES) is False, value

    for value in BLOCKED:
        assert is_blocklisted(value, RULES) is True, value
