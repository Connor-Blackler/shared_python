"""A module to help with encrypting passwords"""
import os
import hashlib
import hmac


def is_correct_password(salt: bytes, password_hash: bytes, password: str) -> bool:
    """Code to reverse public hash_password to determine if the password is correct"""
    return hmac.compare_digest(
        password_hash,
        hashlib.pbkdf2_hmac('sha256', password.encode(),
                            salt=salt, iterations=100000)
    )


def hash_password(password: str) -> tuple[bytes, bytes]:
    """Code to create a salt, and an encryted password returned as a tuple of 
    salt,hashed_password
    """
    generated_salt = os.urandom(16)
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt=generated_salt, iterations=100000)
    return generated_salt, hashed_password
