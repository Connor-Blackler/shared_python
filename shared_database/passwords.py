"""A module to help with encrypting passwords"""
import os
import hashlib
import hmac


def is_correct_password(salt: bytes, password_hash: bytes, password: str) -> bool:
    """
    Check if the provided password matches the hashed password.
    Args:
        salt: The salt used in hashing the password.
        password_hash: The hashed password.
        password: The password to be checked.

    Returns:
        True if the provided password matches the hashed password, False otherwise.
    """
    return hmac.compare_digest(
        password_hash,
        hashlib.pbkdf2_hmac('sha256', password.encode(),
                            salt=salt, iterations=100000)
    )


def hash_password(password: str) -> tuple[bytes, bytes]:
    """
    Hash a password and generate a random salt.
    Args:
    password: The password to be hashed.

    Returns:
        A tuple containing the generated salt and the hashed password.
    """
    generated_salt = os.urandom(16)
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt=generated_salt, iterations=100000)
    return generated_salt, hashed_password
