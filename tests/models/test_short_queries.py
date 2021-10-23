from datetime import datetime, timedelta
from re import IGNORECASE
from re import compile as re_compile

from pytest import mark

from shorter.models.short import Short


@mark.usefixtures("session")
class TestShortQueries:
    @staticmethod
    def test_ordered():
        assert Short.query.count() == 0
        now = datetime.utcnow()

        one = Short.generate(
            target="one",
            delay=2,
            created=now - timedelta(seconds=1),
        )
        two = Short.generate(
            target="two",
            delay=1,
            created=now - timedelta(seconds=3),
        )
        thr = Short.generate(
            target="thr",
            delay=3,
            created=now - timedelta(seconds=2),
        )
        assert Short.query.count() == 3

        assert Short.ordered("PRIME") is None
        assert Short.ordered("BANANA") is None
        assert Short.ordered(None).all() == [one, two, thr]  # same as prime

        assert Short.ordered("prime").all() == [one, two, thr]
        assert Short.ordered("prime", rev=True).all() == [thr, two, one]

        assert Short.ordered("delay").all() == [two, one, thr]
        assert Short.ordered("delay", rev=True).all() == [thr, one, two]

        assert Short.ordered("target").all() == [one, thr, two]
        assert Short.ordered("target", rev=True).all() == [two, thr, one]

        assert Short.ordered("created").all() == [two, thr, one]
        assert Short.ordered("created", rev=True).all() == [one, thr, two]

        assert Short.ordered("active").all() == [one, two, thr]
        assert Short.ordered("active", rev=True).all() == [thr, two, one]

    @staticmethod
    def test_ordered_query():
        assert Short.query.count() == 0
        Short.generate(target="one", delay=0)
        Short.generate(target="two", delay=0)
        Short.generate(target="drop", delay=1)
        Short.generate(target="nope", delay=2)
        assert Short.query.count() == 4

        assert Short.ordered(None).count() == 4
        query = Short.query.filter(Short.delay == 0)
        assert query.count() == 2
        assert Short.ordered(None, query=query).count() == 2

    @staticmethod
    def test_searched():
        assert Short.query.count() == 0
        one = Short.create(symbol="one", target="_cherry", delay=3)
        two = Short.create(symbol="two", target="_eggplant", delay=2)
        thr = Short.create(symbol="thr", target="_peach", delay=1)
        assert Short.query.count() == 3

        assert Short.searched("one").all() == [one]
        assert Short.searched("two").all() == [two]

        assert Short.searched("err").all() == [one]
        assert Short.searched("egg").all() == [two]

        assert Short.searched("t").all() == [two, thr]
        assert Short.searched("p").all() == [two, thr]
        assert Short.searched("_").all() == [one, two, thr]
        assert Short.searched("_", rev=True).all() == [thr, two, one]

        assert Short.searched("_", field="delay", rev=False).all() == [
            thr,
            two,
            one,
        ]
        assert Short.searched("_", field="delay", rev=True).all() == [
            one,
            two,
            thr,
        ]

    @staticmethod
    def test_blocked():
        blocklist = [re_compile(r"^.+example\.com$", IGNORECASE)]
        assert Short.query.count() == 0
        Short.generate(target="http://www.example.org")
        Short.generate(target="https://example.org")
        one = Short.generate(target="http://www.example.com")
        two = Short.generate(target="https://example.com")
        assert Short.query.count() == 4

        assert Short.blocked([]).all() == []
        assert Short.blocked(blocklist).all() == [one, two]
        assert Short.blocked(blocklist, rev=True).all() == [two, one]
