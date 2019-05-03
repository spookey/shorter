from werkzeug.routing import BaseConverter

from shorter.start.environment import SYM_MINI, SYM_POOL


class SymbolConverter(BaseConverter):
    def __init__(self, url_map):
        super(SymbolConverter, self).__init__(url_map)
        self.regex = '(?:{pool}){{{mini},}}'.format(
            pool='|'.join(sym for sym in SYM_POOL),
            mini=SYM_MINI
        )
