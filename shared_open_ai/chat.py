"""A module that allows the user to chat with OpenAi chat using gpt-3.5-turbo"""

import openai
from dataclasses import dataclass
from .get_api_key import OpenAIApiKey
from ._params import Role,Model

@dataclass
class _message():
    role: Role
    content: str

    def generate_request_str(self) -> dict:
        return {"role":str(self.role), "content":self.content}

@dataclass
class _open_ai_conversation():
    _chat_context: list[_message] = []

    def generate_request_str(self) -> dict:
        ...

class openAi():
    def __init__(self, model: Model = Model.GPT35) -> None:
        self.model = model
        self.__conversation = _open_ai_conversation()
        self.__API_KEY = OpenAIApiKey().get_api_key()

    def send_message(self, message: str) -> str:
        ...

    def conversation(self) -> str:
        ...
