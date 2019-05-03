from werkzeug.routing import BaseConverter

from shorter.start.environment import CRAWLERS, SYM_MINI, SYM_POOL


class SymbolConverter(BaseConverter):
    def __init__(self, url_map):
        super(SymbolConverter, self).__init__(url_map)
        self.regex = '(?:{pool}){{{mini},}}'.format(
            pool='|'.join(sym for sym in SYM_POOL),
            mini=SYM_MINI
        )


def is_botagent(user_agent):
    browser = user_agent.browser if user_agent.browser else ''
    string = user_agent.string if user_agent.string else ''

    for crawler in CRAWLERS:
        if crawler in browser.lower():
            return True
        if crawler in string.lower():
            return True

    return False
