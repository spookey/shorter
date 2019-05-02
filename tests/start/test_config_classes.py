from shorter.start.config import (
    BaseConfig, DevelopmentConfig, ProductionConfig, TestingConfig
)
from shorter.start.environment import TITLE


def test_base_config():
    conf = BaseConfig()

    assert conf.DEBUG is False
    assert conf.SECRET_KEY and isinstance(conf.SECRET_KEY, (str, bytes))
    assert conf.TESTING is False
    assert conf.TITLE == TITLE
    assert conf.WTF_CSRF_ENABLED is True


def test_devel_config():
    conf = DevelopmentConfig()

    assert conf.DEBUG is True
    assert conf.SQLALCHEMY_DATABASE_URI.startswith('sqlite:////')
    assert conf.TESTING is False
    assert conf.TITLE == TITLE


def test_test_config():
    conf = TestingConfig()

    assert conf.DEBUG is False
    assert conf.SQLALCHEMY_DATABASE_URI == 'sqlite://'
    assert conf.TESTING is True
    assert conf.TITLE == TITLE


def test_prod_config():
    conf = ProductionConfig()

    assert conf.DEBUG is False
    assert conf.SQLALCHEMY_DATABASE_URI == 'sqlite://'
    assert conf.TESTING is False
    assert conf.TITLE == TITLE
