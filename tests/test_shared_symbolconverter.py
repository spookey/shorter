from random import choice
from string import punctuation

from werkzeug.routing import Map, Rule

from shorter.shared import SymbolConverter
from shorter.start.environment import SYM_MINI, SYM_POOL


def test_symbolconverter():
    rule = Rule('/<symbol:symb>')
    assert Map(rules=[rule], converters={'symbol': SymbolConverter})

    def _m(inp):
        match = rule.match('|/{}'.format(inp))
        if match is not None:
            return match.get('symb', None)
        return None

    for _ in range(42):
        size = choice(range(SYM_MINI, SYM_MINI + 1337))
        sym = ''.join(choice(SYM_POOL) for _ in range(size))
        assert _m(sym) == sym

    for _ in range(23):
        sym = ''.join(choice(SYM_POOL) for _ in range(SYM_MINI - 1))
        assert _m(sym) is None

    for _ in range(5):
        sym = '/'.join(choice(SYM_POOL) for _ in range(SYM_MINI))
        assert _m(sym) is None

    for pun in punctuation:
        sym = ''.join((
            ''.join(choice(SYM_POOL) for _ in range(SYM_MINI - 1)),
            pun
        ))
        assert _m(sym) is None
