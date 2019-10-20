from werkzeug.routing import BaseConverter
from wtforms.validators import ValidationError

from shorter.start.config import url_blocklist
from shorter.start.environment import CRAWLERS, SOCIAL, SYM_MINI, SYM_POOL

BLOCKLIST = url_blocklist()


class SymbolConverter(BaseConverter):
    def __init__(self, url_map):
        super(SymbolConverter, self).__init__(url_map)
        self.regex = '(?:{pool}){{{mini},}}'.format(
            pool='|'.join(sym for sym in SYM_POOL),
            mini=SYM_MINI
        )


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

    def __call__(self, _, field):
        if self.is_blocked(field.data):
            raise ValidationError('Not possible this time!')
