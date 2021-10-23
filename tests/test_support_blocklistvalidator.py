from re import IGNORECASE
from re import compile as re_compile

from pytest import raises
from wtforms.validators import ValidationError

from shorter.support import BlocklistValidator

RULES = [
    re_compile(line, IGNORECASE)
    for line in (
        r"^.+example\.com$",
        r"^http:.+",
        r".+what\/ever",
        r".+\d{4,}",
    )
]
ALLOWED = (
    "https://www.example.org",
    "https://www.example.com/",
    "https://www.example.org/whatever",
    "https://www.example.org/123",
)
BLOCKED = (
    "http://www.example.org",
    "https://www.example.com",
    "https://www.example.org/what/ever",
    "https://www.example.org/12345",
)


def _phony_field(data):
    def field():
        pass

    field.data = data
    return field


def _phony_short(prime, target):
    def short():
        pass

    short.prime = prime
    short.target = target
    return short


def test_validator_empty():
    validator = BlocklistValidator([])

    for value in [fl for at in [ALLOWED, BLOCKED] for fl in at]:
        assert validator.is_blocked(value) is False, value


def test_validator_is_blocked():
    validator = BlocklistValidator(RULES)
    for value in ALLOWED:
        assert validator.is_blocked(value) is False, value

    for value in BLOCKED:
        assert validator.is_blocked(value) is True, value


def test_validator_prime_targets():
    validator = BlocklistValidator(RULES)

    allow = [_phony_short(num, tgt) for num, tgt in enumerate(ALLOWED)]
    block = [_phony_short(num, tgt) for num, tgt in enumerate(BLOCKED)]

    allowed = validator.prime_targets(allow)
    blocked = validator.prime_targets(block)

    assert allowed == []
    assert blocked == list(range(len(BLOCKED)))


def test_validator_call():
    validator = BlocklistValidator(RULES)

    for value in ALLOWED:
        assert validator(None, _phony_field(value)) is None

    for value in BLOCKED:
        with raises(ValidationError) as verr:
            assert validator(None, _phony_field(value)) is None
            assert "not possible" in verr.message.lower()
