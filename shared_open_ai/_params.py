"""A module that stores all parameters used in the OpenAI chat model"""

from enum import Enum


class Model(Enum):
    """An enumeration that emulates openAI.chat.model

    https://platform.openai.com/docs/models/model-endpoint-compatibility
    """
    GPT35 = "gpt-3.5-turbo"
    GPT4 = "gpt-4"


class Role(Enum):
    """An enumeration that emulates openAI.chat.role

    https://platform.openai.com/docs/api-reference/chat
    """
    USER = "user"
    ASSISTANT = "assistant"
