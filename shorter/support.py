from werkzeug.routing import BaseConverter
from wtforms.validators import ValidationError

from shorter.start.config import url_blocklist
from shorter.start.environment import (
    CRAWLERS,
    RX_XSS_STORED,
    SOCIAL,
    SYM_MINI,
    SYM_POOL,
)

BLOCKLIST = url_blocklist(RX_XSS_STORED)


class SymbolConverter(BaseConverter):
    def __init__(self, url_map):
        super().__init__(url_map)

        pool = '|'.join(sym for sym in SYM_POOL)
        self.regex = f'(?:{pool}){{{SYM_MINI},}}'


def _is_agent(user_agent, collection):
    browser = user_agent.browser if user_agent.browser else ''
    string = user_agent.string if user_agent.string else ''

    for elem in collection:
        if elem in browser.lower():
            return True
        if elem in string.lower():
            return True

    return False


def is_botagent(user_agent):
    return _is_agent(user_agent, CRAWLERS)


def is_socialagent(user_agent):
    return _is_agent(user_agent, SOCIAL)


class BlocklistValidator:
    def __init__(self, blocklist):
        self.blocklist = blocklist

    def is_blocked(self, value):
        return any(rule.search(value) for rule in self.blocklist)

    def prime_targets(self, shorts):
        return [
            short.prime for short in shorts
            if self.is_blocked(short.target)
        ]

    def __call__(self, _, field):
        if self.is_blocked(field.data):
            raise ValidationError('Not possible this time!')
