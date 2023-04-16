"""A module that allows the user to chat with OpenAi chat using gpt-3.5-turbo"""

import openai
from dataclasses import dataclass
from .get_api_key import OpenAIApiKey
from ._params import Role,Model

openai.api_key = OpenAIApiKey().get_api_key()

@dataclass
class _Message():
    _role: Role
    _content: str
    request_str = ""

    def __post_init__(self) -> None:
        self.request_str = {"role": f"{self._role.value}","content":f"{self._content}"}

class _OpenAiConversation():
    """A class that emulates an open ai conversation"""
    def __init__(self) -> None:
        self._chat_context: list[_Message] = []

    def as_list(self) -> list:
        """returns the conversation as a list, each entry of the conversation is a dictionary"""
        ret = []
        for this_message in self._chat_context:
            ret.append(this_message.request_str)

        return ret

    def append(self, message: _Message) -> None:
        """Append a new message to the open ai conversation"""
        self._chat_context.append(message)

class OpenAIChat():
    """A class that communicates with the OpenAI model"""
    def __init__(self, model: Model = Model.GPT35) -> None:
        self.model = model
        self.__conversation = _OpenAiConversation()

    def send_message(self, message: str) -> str:
        """Send a message to the openAI, whilst appending to the conversation"""
        self.__conversation.append(_Message(Role.USER, message))

        response = openai.ChatCompletion.create(
            model=self.model.value,
            messages=self.__conversation.as_list())

        assistant_response = response['choices'][0]['message']['content']
        assistant_response = assistant_response.strip("\n").strip()
        self.__conversation.append(_Message(Role.ASSISTANT, assistant_response))

        return assistant_response

    def clear(self) -> None:
        self.__conversation = _OpenAiConversation()
