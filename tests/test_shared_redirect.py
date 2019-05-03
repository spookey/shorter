from random import choice

from shorter.models.short import Short
from shorter.shared import redirect_link, redirect_meta, redirect_script
from shorter.start.environment import SYM_MINI, SYM_POOL


def _sho(target='test', delay=23):
    return Short.create(
        symbol=''.join(choice(SYM_POOL) for _ in range(SYM_MINI)),
        target=target,
        delay=delay,
        _commit=False
    )


def test_meta():
    sho = _sho()
    res = redirect_meta(sho)
    assert '<meta' in res
    assert 'no-referrer' in res
    assert 'refresh' in res
    assert 'content=' in res
    assert 'url=' in res
    assert str(sho.delay) in res
    assert sho.target in res


def test_link():
    sho = _sho()
    res = redirect_link(sho)
    assert '<a' in res
    assert 'nofollow' in res
    assert 'href=' in res
    assert sho.target in res


def test_link_text():
    sho = _sho()
    res = redirect_link(sho, 'demo')
    assert 'href=' in res
    assert sho.target in res
    assert 'demo' in res


def test_script():
    sho = _sho()
    res = redirect_script(sho)
    assert '<script' in res
    assert 'setTimeout' in res
    assert 'window.location.replace' in res
    assert sho.target in res
    assert str(1000 * sho.delay) in res
