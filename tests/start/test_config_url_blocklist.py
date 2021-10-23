from re import compile as re_compile

from shorter.start.config import url_blocklist

RX_TYPE = type(re_compile(r""))


def test_no_list(tmpdir):
    blist = url_blocklist(base=str(tmpdir), filename="no-such-blocklist.txt")
    assert blist == []

    tmpdir.remove()


def text_presets(tmpdir):
    presets = [r"^.+$", r".*"]

    blist = url_blocklist(
        *presets, base=str(tmpdir), filename="empty-blocklist.txt"
    )
    assert len(blist) == 2

    for patt in blist:
        assert isinstance(patt, RX_TYPE)

        assert patt.search("abc")
        assert patt.search("def")

    tmpdir.remove()


def test_list_items(tmpdir):
    name = "testlist.txt"
    tmpdir.join(name).write(
        r"""
# no comment

^ftps?:\/\/.*$
example\.org$
    """.strip(),
        "w",
    )

    blist = url_blocklist(base=str(tmpdir), filename=name)
    assert len(blist) == 2

    for patt in blist:
        assert isinstance(patt, RX_TYPE)

        assert patt.search("ftp://example.org")
        assert patt.search("FTP://EXAMPLE.ORG")
        assert patt.search("ftps://example.org")
        assert patt.search("FTPS://EXAMPLE.ORG")

        assert not patt.search("http://example.com")
        assert not patt.search("http://example.org/one/two")

    tmpdir.remove()
