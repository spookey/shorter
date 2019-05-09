from importlib import reload
from os import path

from shorter.start import environment


def test_database(monkeypatch):
    assert environment.DATABASE == 'sqlite://'
    assert environment.DATABASE_DEV == 'sqlite:///{}'.format(
        path.abspath(path.join(
            environment.ROOT_DIR, 'database_dev.sqlite'
        ))
    )

    monkeypatch.setenv('DATABASE', '🍌')
    monkeypatch.setenv('DATABASE_DEV', '🐵')
    reload(environment)

    assert environment.DATABASE == '🍌'
    assert environment.DATABASE_DEV == '🐵'


def test_loglevel(monkeypatch):
    assert environment.LOG_LVL == 'info'

    monkeypatch.setenv('LOG_LVL', '🎙')
    reload(environment)

    assert environment.LOG_LVL == '🎙'


def test_secret(monkeypatch):
    assert environment.SECRET_BASE == environment.ROOT_DIR
    assert environment.SECRET_FILE == 'secret.key'

    monkeypatch.setenv('SECRET_BASE', '💯')
    monkeypatch.setenv('SECRET_FILE', '🧦')
    reload(environment)

    assert environment.SECRET_BASE == '💯'
    assert environment.SECRET_FILE == '🧦'


def test_theme(monkeypatch):
    assert environment.THEME == 'default'

    monkeypatch.setenv('THEME', '🗻')
    reload(environment)

    assert environment.THEME == '🗻'


def test_title(monkeypatch):
    assert environment.TITLE == environment.APP_NAME

    monkeypatch.setenv('TITLE', '🎱')
    reload(environment)

    assert environment.TITLE == '🎱'


def test_language(monkeypatch):
    assert environment.HTML_LANG == 'en'

    monkeypatch.setenv('HTML_LANG', '🏁')
    reload(environment)

    assert environment.HTML_LANG == '🏁'


def test_delay(monkeypatch):
    assert environment.DELAY_DEF == 5
    assert environment.DELAY_MAX == 60

    monkeypatch.setenv('DELAY_DEF', '⏳')
    monkeypatch.setenv('DELAY_MAX', '💯')
    reload(environment)

    assert environment.DELAY_DEF == 5
    assert environment.DELAY_MAX == 60

    monkeypatch.setenv('DELAY_DEF', '42')
    monkeypatch.setenv('DELAY_MAX', '1337')
    reload(environment)

    assert environment.DELAY_DEF == 42
    assert environment.DELAY_MAX == 1337


def test_symbol_minimum(monkeypatch):
    assert environment.SYM_MINI == 3

    monkeypatch.setenv('SYM_MINI', '5️⃣')
    reload(environment)

    assert environment.SYM_MINI == 3

    monkeypatch.setenv('SYM_MINI', '5')
    reload(environment)

    assert environment.SYM_MINI == 5
