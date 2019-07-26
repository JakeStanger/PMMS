import helpers


def test_default_generate_secret_key():
    key = helpers.generate_secret_key()
    assert type(key) == str
    assert len(key) == 64


def test_variable_secret_key():
    key = helpers.generate_secret_key(4)
    assert type(key) == str
    assert len(key) == 4
