from .hmac import Digestable
import uuid


def test_digestable() -> None:
    my_digest_key = "special key"
    my_digest = Digestable(my_digest_key)

    for i in range(20):
        special_data = str(uuid.uuid4()).encode("utf-8")
        data = my_digest.make_digest(special_data)

        assert data == my_digest.make_digest(special_data)

        # Insert a new character to special data
        altered_data = special_data.decode("utf-8") + "a"
        assert altered_data.encode(
            "utf-8") != my_digest.make_digest(special_data)
