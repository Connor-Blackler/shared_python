import os
from pytest import MonkeyPatch
from shared_passwords.shared_password import PasswordRepo


def my_password() -> str:
    return "124651234512"


def __password_file_path() -> str:
    path = os.getenv('APPDATA')
    return path + "\\shared_repo\\OpenAI\\API_KEY_UNIT_TEST_FALSE"


def test_get_api_key_false(monkeypatch: MonkeyPatch) -> None:
    inputs = [my_password()]
    monkeypatch.setattr("builtins.input", lambda: inputs.pop(0))
    monkeypatch.setattr(
        PasswordRepo(), "_PasswordRepo__password_file_path", __password_file_path)

    assert "4363463463463" != PasswordRepo().get_password_key("TEST_PASSWORD")


def test_get_api_key_true(monkeypatch: MonkeyPatch) -> None:
    inputs = [my_password()]
    monkeypatch.setattr("builtins.input", lambda: inputs.pop(0))
    monkeypatch.setattr(
        PasswordRepo(), "_PasswordRepo__password_file_path", __password_file_path)

    assert my_password() == PasswordRepo().get_password_key("TEST_PASSWORD")
