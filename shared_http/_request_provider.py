"""A module that contains different request protocols hidden to the outside"""

import http.client
from abc import ABC, abstractmethod
import httpx
from .request_params import RequestResponse,Url,ProtocolType

class RequestProtocol(ABC):
    """An abstract class for a request protocol"""
    @staticmethod
    @abstractmethod
    def protocol_type() -> ProtocolType:
        """Declares the Porotol type of this object"""

    @abstractmethod
    def get(self, this_url: Url) -> RequestResponse:
        """Method that handles the request"""

class _Https(RequestProtocol):
    @staticmethod
    def protocol_type() -> ProtocolType:
        return ProtocolType.HTTPS

    def get(self, this_url: Url) -> RequestResponse:
        print("Start GET: https")
        client = http.client.HTTPSConnection(host=self.__trim_host(this_url.host))
        client.request("GET", this_url.url)
        response = client.getresponse()
        print("End GET: https")
        my_response = response.read()
        client.close()
        return RequestResponse("", my_response.decode("ISO-8859-1"),
                               "", response.status)

    def __trim_host(self, host: str) -> str:
        if host.startswith("https://"):
            host = host[8:]

        if host.endswith("/"):
            host = host[:-1]

        return host

class _Httpx(RequestProtocol):
    @staticmethod
    def protocol_type() -> ProtocolType:
        return ProtocolType.HTTPX

    def get(self, this_url: Url) -> RequestResponse:
        print("Start GET: httpx")
        client = httpx.Client()
        response = client.get(this_url.host + this_url.url)
        print("End GET: httpx")
        return RequestResponse(response.text, response.content,
                               response.encoding, response.status_code)

class RequestFactory:
    """A factory that produces a suitable request protocol"""
    def _get_protocols(self) -> tuple[RequestProtocol]:
        """An array of all available protocols"""
        return (_Https,_Httpx)

    def get_protocol(self, protocol_type: ProtocolType) -> RequestProtocol:
        """iterates through available different protocols to find the matching protocol 
        to use for this request
        
        """
        for i in self._get_protocols():
            if i.protocol_type() == protocol_type:
                return i
