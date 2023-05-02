"""A decorator that ensures memento design pattern

Use: save / restore
"""


def _get_properties(obj) -> list[str]:
    return [prop for prop in dir(obj) if not prop.startswith('__') and not callable(getattr(obj, prop))]


def _get_properties_d(obj, properties: list[str]) -> dict:
    ret = {}

    for prop in properties:
        ret[prop] = getattr(obj, prop)

    return ret


def memento(cls):
    def save(self):
        print("save state")
        self.__saved_states.append(
            _get_properties_d(self, _get_properties(self)))

    def restore(self):
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
