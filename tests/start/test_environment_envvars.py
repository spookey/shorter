from importlib import reload
from os import path

from shorter.start import environment


def test_database(monkeypatch):
    db_dev = path.abspath(
        path.join(environment.ROOT_DIR, "database_dev.sqlite")
    )
    assert environment.DATABASE == "sqlite://"
    assert environment.DATABASE_DEV == f"sqlite:///{db_dev}"

    monkeypatch.setenv("DATABASE", "🍌")
    monkeypatch.setenv("DATABASE_DEV", "🐵")
    reload(environment)

    assert environment.DATABASE == "🍌"
    assert environment.DATABASE_DEV == "🐵"


def test_loglevel(monkeypatch):
    assert environment.LOG_LVL == "info"

    monkeypatch.setenv("LOG_LVL", "🎙")
    reload(environment)

    assert environment.LOG_LVL == "🎙"


def test_secret(monkeypatch):
    assert environment.SECRET_BASE == environment.ROOT_DIR
    assert environment.SECRET_FILE == "secret.key"

    monkeypatch.setenv("SECRET_BASE", "💯")
    monkeypatch.setenv("SECRET_FILE", "🧦")
    reload(environment)

    assert environment.SECRET_BASE == "💯"
    assert environment.SECRET_FILE == "🧦"


def test_blocklist(monkeypatch):
    assert environment.BLOCK_BASE == environment.ROOT_DIR
    assert environment.BLOCK_FILE == "blocklist.txt"

    monkeypatch.setenv("BLOCK_BASE", "📥")
    monkeypatch.setenv("BLOCK_FILE", "💌")
    reload(environment)

    assert environment.BLOCK_BASE == "📥"
    assert environment.BLOCK_FILE == "💌"


def test_csrf_strict(monkeypatch):
    assert environment.CSRF_STRICT is True

    monkeypatch.setenv("CSRF_STRICT", "🎩")
    reload(environment)

    assert environment.CSRF_STRICT is True


def test_theme(monkeypatch):
    assert environment.THEME == "default"

    monkeypatch.setenv("THEME", "🗻")
    reload(environment)

    assert environment.THEME == "🗻"


def test_title(monkeypatch):
    assert environment.TITLE == environment.APP_NAME

    monkeypatch.setenv("TITLE", "🎱")
    reload(environment)

    assert environment.TITLE == "🎱"


def test_language(monkeypatch):
    assert environment.HTML_LANG == "en"

    monkeypatch.setenv("HTML_LANG", "🏁")
    reload(environment)

    assert environment.HTML_LANG == "🏁"


def test_delay(monkeypatch):
    assert environment.DELAY_MIN == 0
    assert environment.DELAY_MAX == 30
    assert environment.DELAY_DEF == 6
    assert environment.DELAY_STP == 3

    monkeypatch.setenv("DELAY_MIN", "0️⃣")
    monkeypatch.setenv("DELAY_MAX", "💯")
    monkeypatch.setenv("DELAY_DEF", "⏳")
    monkeypatch.setenv("DELAY_STP", "🔀")
    reload(environment)

    assert environment.DELAY_MIN == 0
    assert environment.DELAY_MAX == 30
    assert environment.DELAY_DEF == 6
    assert environment.DELAY_STP == 3

    monkeypatch.setenv("DELAY_MIN", "23")
    monkeypatch.setenv("DELAY_MAX", "1337")
    monkeypatch.setenv("DELAY_DEF", "42")
    monkeypatch.setenv("DELAY_STP", "5")
    reload(environment)

    assert environment.DELAY_MIN == 23
    assert environment.DELAY_MAX == 1337
    assert environment.DELAY_DEF == 42
    assert environment.DELAY_STP == 5


def test_symbol_minimum(monkeypatch):
    assert environment.SYM_MINI == 3

    monkeypatch.setenv("SYM_MINI", "5️⃣")
    reload(environment)

    assert environment.SYM_MINI == 3

    monkeypatch.setenv("SYM_MINI", "5")
    reload(environment)

    assert environment.SYM_MINI == 5


def test_pagination(monkeypatch):
    assert environment.PAGINATION == 100

    monkeypatch.setenv("PAGINATION", "🎱")
    reload(environment)

    assert environment.PAGINATION == 100

    monkeypatch.setenv("PAGINATION", "42")
    reload(environment)

    assert environment.PAGINATION == 42
