"""objects used when sending requests"""

from dataclasses import dataclass
from enum import Enum,auto

@dataclass
class Url:
    """"A dataclass that represents a URL"""
    host: str = ""
    url: str = ""

@dataclass
class RequestResponse:
    """"A dataclass that represents the response from a url request"""
    text: str = ""
    content: str = ""
    encoding: str = ""
    status_code: str = ""

class ProtocolType(Enum):
    """"Represents the available different protocols in the back-end"""
    HTTPS = auto()
    HTTPX = auto()
