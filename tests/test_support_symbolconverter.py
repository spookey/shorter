from random import choice
from string import punctuation

from werkzeug.exceptions import NotFound
from werkzeug.routing import Map, Rule

from shorter.start.environment import SYM_MINI, SYM_POOL
from shorter.support import SymbolConverter


def test_symbolconverter():
    rule = Rule("/<symbol:symb>")
    url_map = Map(rules=[rule], converters={"symbol": SymbolConverter})
    adapter = url_map.bind("localhost", "/")

    def _m(inp):
        try:
            (  # pylint: disable=unpacking-non-sequence
                view,
                mapped,
            ) = adapter.match(f"/{inp}")
            assert view is None
            return mapped.get("symb")
        except NotFound:
            return None

    for _ in range(42):
        size = choice(range(SYM_MINI, SYM_MINI + 1337))
        sym = "".join(choice(SYM_POOL) for _ in range(size))
        assert _m(sym) == sym

    for _ in range(23):
        sym = "".join(choice(SYM_POOL) for _ in range(SYM_MINI - 1))
        assert _m(sym) is None

    for _ in range(5):
        sym = "/".join(choice(SYM_POOL) for _ in range(SYM_MINI))
        assert _m(sym) is None

    for pun in punctuation:
        sym = "".join(
            ("".join(choice(SYM_POOL) for _ in range(SYM_MINI - 1)), pun)
        )
        assert _m(sym) is None
