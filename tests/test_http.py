from shared_http.request import get
from shared_http.request_params import Url, ProtocolType


def test_Url() -> None:
    data = Url()
    assert data.host == ""
    assert data.url == ""

    data = Url(host="test", url="test2")
    assert data.host == "test"
    assert data.url == "test2"


def test_get() -> None:
    result = get(Url("https://www.google.co.uk", ""))
    assert result.status_code == 200

    result2 = get(Url("https://www.google.co.uk", ""),
                  protocol_type=ProtocolType.HTTPS)
    assert result2.status_code == 200
