"""A decorator that ensures observer design pattern

Use: subscribe / unsubscribe / update methods
"""
from __future__ import annotations
from typing import Protocol
from abc import ABC, abstractmethod


class observer(Protocol):
    def update(self, subject: abstract_subject) -> None:
        ...


class abstract_subject(ABC):
    @abstractmethod
    def subscribe(self, my_observer: observer) -> None:
        ...

    @abstractmethod
    def unsubscribe(self, my_observer: observer) -> None:
        ...

    @abstractmethod
    def update(self) -> None:
        ...


def observer(cls):
    def subscribe(self, my_observer: observer) -> None:
        if not my_observer in self.__observers:
            self.__observers.append(my_observer)

    def unsubscribe(self, my_observer: observer) -> None:
        if my_observer in self.__observers:
            self.__observers.remove(my_observer)

    def update(self) -> None:
        for this_observer in self.__observers:
            this_observer.update(self)

    setattr(cls, "__observers", [])
    setattr(cls, "subscribe", subscribe)
    setattr(cls, "unsubscribe", unsubscribe)
    setattr(cls, "update", update)

    def wrapper(*args, **kwargs):
        return cls(*args, **kwargs)

    return wrapper
