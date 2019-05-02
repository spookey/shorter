from flask import render_template
from werkzeug.routing import BaseConverter

from shorter.start.environment import SYM_MINI, SYM_POOL


def errorhandler(error):
    return render_template(
        'error.html',
        error=error,
        title=error.code,
    ), error.code


class SymbolConverter(BaseConverter):
    def __init__(self, url_map):
        super(SymbolConverter, self).__init__(url_map)
        self.regex = '(?:{pool}){{{mini},}}'.format(
            pool='|'.join(sym for sym in SYM_POOL),
            mini=SYM_MINI
        )
