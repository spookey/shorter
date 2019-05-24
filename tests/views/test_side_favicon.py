from flask import url_for
from pytest import mark

FAV_URLS = ('/favicon.png', '/favicon.ico', '/logo.png')


@mark.usefixtures('ctx_app')
def test_favicon_url():
    assert url_for('side.favicon') == FAV_URLS[0]
    assert url_for('side.logo') == FAV_URLS[-1]


def test_favicon_content(client):
    org = client.get(url_for('static', filename='favicon.png'))
    req = client.get(url_for('side.favicon'))
    assert org.data == req.data


def test_favicon_by_url(client):
    for url in FAV_URLS:
        res = client.get(url)
        assert res.status_code == 200
        assert res.mimetype == 'image/png'
