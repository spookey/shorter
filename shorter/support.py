from werkzeug.routing import BaseConverter

from shorter.start.environment import CRAWLERS, SOCIAL, SYM_MINI, SYM_POOL


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
