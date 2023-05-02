"""A module that combines hmac and pickle"""
import hashlib
import hmac


class Digestable():
    """Digest a message with a digest key"""

    def __init__(self, digest_key: str) -> None:
        self._digest_key = digest_key.encode("utf-8")

    def make_digest(self, data: str) -> str:
        """digest the message"""
        ret = hmac.new(self._digest_key,
                       data,
                       hashlib.sha1)

        return ret.hexdigest()
