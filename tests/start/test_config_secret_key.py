from os import urandom

from shorter.start.config import secret_key


def test_key_read(tmpdir):
    name = "secret-test-read.key"
    secret = urandom(128)
    tmpdir.join(name).write(secret, "wb")

    assert secret_key(base=str(tmpdir), filename=name) == secret
    tmpdir.remove()


def test_key_write(tmpdir):
    name = "secret-test-write.key"
    tmpkey = tmpdir.join(name)

    assert secret_key(base=str(tmpdir), filename=name) == tmpkey.read("rb")
    tmpdir.remove()
