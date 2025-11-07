from auth import utils


def test_hash_password():
    password = "Testpassword123"
    hashed_password = utils.hash_password(password=password)
    assert type(hashed_password) is str
    assert hashed_password != password
    assert len(hashed_password) == 60
    assert utils.validate_password(
        password=password,
        hashed_password=hashed_password,
    )
