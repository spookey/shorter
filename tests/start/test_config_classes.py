from shorter.start.config import (
    BaseConfig, DevelopmentConfig, ProductionConfig, TestingConfig
)


def test_base_config():
    conf = BaseConfig()

    assert conf.APP_NAME == 'shrtr'
    assert conf.DEBUG is False
    assert conf.SECRET_KEY and isinstance(conf.SECRET_KEY, (str, bytes))
    assert conf.TESTING is False
    assert conf.WTF_CSRF_ENABLED is True


def test_devel_config():
    conf = DevelopmentConfig()

    assert conf.APP_NAME == 'shrtr'
    assert conf.DEBUG is True
    assert conf.SQLALCHEMY_DATABASE_URI.startswith('sqlite:////')
    assert conf.TESTING is False


def test_test_config():
    conf = TestingConfig()

    assert conf.APP_NAME == 'shrtr'
    assert conf.DEBUG is False
    assert conf.SQLALCHEMY_DATABASE_URI == 'sqlite://'
    assert conf.TESTING is True


def test_prod_config():
    conf = ProductionConfig()

    assert conf.APP_NAME == 'shrtr'
    assert conf.DEBUG is False
    assert conf.SQLALCHEMY_DATABASE_URI == 'sqlite://'
    assert conf.TESTING is False
