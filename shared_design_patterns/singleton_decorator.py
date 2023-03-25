"""A decorator that ensures singleton desing pattern"""
def singleton(this_class):
    singleton_instances = {}
    def get_instance():
        if this_class not in singleton_instances:
            singleton_instances[this_class] = this_class()
        return singleton_instances[this_class]
    return get_instance