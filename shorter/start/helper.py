from logging import getLogger

LOG = getLogger(__name__)


def parse_int(value, fallback=0, warn=True):
    try:
        value = int(value)
    except (ValueError, TypeError) as ex:
        if warn:
            LOG.exception(ex)
            LOG.warning(
                'cannot parse "%s" - using fallback "%s"',
                value, fallback
            )
        value = fallback
    return value
