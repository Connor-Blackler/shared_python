"""The main module to demonstrate the decorator design pattern"""
import time


def time_fn(fn):
    """
    Decorator function that adds timing functionality to the decorated function.
    Args:
    fn: The function to be decorated.

    Returns:
        The decorated function.
    """
    def wrapper(*args, **kwargs):
        """
        Wrapper function that measures the execution time of the decorated function.

        Args:
            *args: Positional arguments to be passed to the decorated function.
            **kwargs: Keyword arguments to be passed to the decorated function.
        """
        start_time = time.time()
        fn(*args, **kwargs)
        print(f"fn took: {time.time() - start_time} seconds")

    return wrapper


def logger_fn(fn):
    """
    Decorator function that adds logging functionality to the decorated function.
    Args:
        fn: The function to be decorated.

    Returns:
        The decorated function.
    """
    def wrapper(*args, **kwargs):
        """
        Wrapper function that logs the arguments and returns the result of the decorated function.

        Args:
            *args: Positional arguments to be passed to the decorated function.
            **kwargs: Keyword arguments to be passed to the decorated function.

        Returns:
            The result of the decorated function.
        """
        print("logging to a file: " + " ".join([str(arg) for arg in args]))
        return fn(*args, **kwargs)

    return wrapper
