from shared_open_ai.get_api_key import OpenAIApiKey

def test_get_api_key() -> None:
    open_ai_api_key = OpenAIApiKey()
    print(open_ai_api_key.get_api_key())

test_get_api_key()