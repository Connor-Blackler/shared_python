from .singleton_decorator import singleton


def test_singleton_decorator() -> None:
    @singleton
    class bob():
        ...

    a, b = bob(), bob()
    assert a is b
