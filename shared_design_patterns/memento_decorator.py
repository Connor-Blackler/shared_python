"""
A decorator that ensures memento design pattern.

The memento design pattern allows saving and restoring the state of an object.

Usage: save / restore
"""


def _get_properties(obj) -> list[str]:
    """
    Helper function to get the properties of an object.
    Args:
    obj: The object.

    Returns:
        A list of property names.
    """
    return [prop for prop in dir(obj) if not prop.startswith('__') and not callable(getattr(obj, prop))]


def _get_properties_d(obj, properties: list[str]) -> dict:
    """
    Helper function to get the values of specific properties of an object.
    Args:
    obj: The object.
    properties: A list of property names.

    Returns:
        A dictionary mapping property names to their values.
    """
    ret = {}

    for prop in properties:
        ret[prop] = getattr(obj, prop)

    return ret


def memento(cls):
    """
    Decorator function that adds memento functionality to a class.
    Args:
        cls: The class to be decorated.

    Returns:
        The decorated class.
    """

    def save(self):
        """Saves the state of the object."""
        print("save state")
        self.__saved_states.append(
            _get_properties_d(self, _get_properties(self)))

    def restore(self):
        """Restores the state of the object."""
        if len(self.__saved_states) == 0:
            print("no states to restore")
            return

        print("restore state")
        my_state = self.__saved_states.pop()

        for this_prop in _get_properties(self):
            setattr(self, this_prop, my_state[this_prop])

    setattr(cls, "__saved_states", [])
    setattr(cls, "save", save)
    setattr(cls, "restore", restore)

    def wrapper(*args, **kwargs):
        return cls(*args, **kwargs)

    return wrapper
