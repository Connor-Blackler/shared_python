from pytest import MonkeyPatch
from shared_open_ai.get_api_key import OpenAIApiKey
import os


def my_api_key() -> str:
    return "124651234512"


def test_get_api_key_false(monkeypatch: MonkeyPatch) -> None:
    def _get_api_key_location(self) -> str:
        path = os.getenv('APPDATA')
        return path + "\\shared_repo\\OpenAI\\API_KEY_UNIT_TEST_FALSE"

    inputs = [my_api_key(), "y"]
    monkeypatch.setattr("builtins.input", lambda: inputs.pop(0))
    monkeypatch.setattr(
        OpenAIApiKey, "_OpenAIApiKey__api_path", _get_api_key_location)

    open_ai_api_key = OpenAIApiKey(False)
    assert open_ai_api_key.get_api_key() == my_api_key()


def test_get_api_key_true(monkeypatch: MonkeyPatch) -> None:
    def _get_api_key_location(self) -> str:
        path = os.getenv('APPDATA')
        return path + "\\shared_repo\\OpenAI\\API_KEY_UNIT_TEST_TRUE"

    inputs = [my_api_key(), "y"]
    monkeypatch.setattr("builtins.input", lambda: inputs.pop(0))
    monkeypatch.setattr(
        OpenAIApiKey, "_OpenAIApiKey__api_path", _get_api_key_location)

    open_ai_api_key = OpenAIApiKey(True)
    assert open_ai_api_key.get_api_key() == my_api_key()
