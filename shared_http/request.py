"""Request a URL via GET

"""

from typing import Callable
from concurrent.futures import ThreadPoolExecutor
from .request_params import RequestResponse,Url
from ._request_provider import ProtocolType,RequestFactory

ResponseCallback = Callable[[RequestResponse], None]
_pool = ThreadPoolExecutor()
_my_request_factory = RequestFactory()

def __get_req(this_url: Url, callback: ResponseCallback, protocol_type: ProtocolType) -> None:
    request = _my_request_factory.get_protocol(protocol_type)()
    callback(request.get(this_url))

def get_async(this_url: Url, callback: ResponseCallback, protocol_type: ProtocolType = ProtocolType.HTTPX):
    _pool.submit(__get_req, this_url, callback, protocol_type)

def get(this_url: Url, protocol_type: ProtocolType = ProtocolType.HTTPX) -> RequestResponse:
    global RET

    def my_response(response: RequestResponse) -> None:
        global RET
        RET = response

    __get_req(this_url, my_response, protocol_type)

    my_ret = RET
    del RET
    return my_ret
