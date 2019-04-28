from os import path

from pytest import raises

from shorter.start.config import theme_folders
from shorter.start.environment import ROOT_DIR


def test_theme_folders_default():
    stat, tmpl = theme_folders()

    assert stat == path.join(ROOT_DIR, 'themes', 'default', 'static')
    assert tmpl == path.join(ROOT_DIR, 'themes', 'default', 'templates')


def test_theme_folders_plain():
    stat, tmpl = theme_folders(theme='plain')

    assert stat == path.join(ROOT_DIR, 'themes', 'plain', 'static')
    assert tmpl == path.join(ROOT_DIR, 'themes', 'plain', 'templates')


def test_theme_folders_error(tmpdir):
    def _action():
        return theme_folders(root=str(tmpdir), theme='test')

    def _check():
        with raises(RuntimeError):
            _action()

    _check()

    theme_path = tmpdir.join('themes')
    theme_path.mkdir()
    _check()

    test_path = theme_path.join('test')
    test_path.mkdir()
    _check()

    stat_path = test_path.join('static')
    stat_path.mkdir()
    tmpl_path = test_path.join('templates')
    tmpl_path.mkdir()

    stat, tmpl = _action()

    assert stat == str(stat_path)
    assert tmpl == str(tmpl_path)

    tmpdir.remove()
