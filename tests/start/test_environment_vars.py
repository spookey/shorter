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
