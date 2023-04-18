from shared_database.passwords import is_correct_password, hash_password
import uuid


def test_password_hashing() -> None:
    for i in range(20):
        this_password = str(uuid.uuid4())
        this_salt, this_hashed_password = hash_password(this_password)

        assert is_correct_password(
            this_salt, this_hashed_password, str(uuid.uuid4())) is False
        assert is_correct_password(
            this_salt, this_hashed_password, this_password) is True
