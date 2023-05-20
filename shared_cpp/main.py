import ctypes
from shared_decorators.main import time_fn


def create_image(width: int, height: int):
    """
    Create an image with the specified width and height.

    Args:
        width: The width of the image.
        height: The height of the image.

    Returns:
        A ctypes array representing the image data.
    """
    num_elements = width * height

    # Create a ctypes array of int8 to represent the image data
    image_data = (ctypes.c_uint8 * (num_elements * 4))()

    for i in range(0, num_elements * 4, 4):
        image_data[i] = 255  # red
        image_data[i + 1] = 50  # green
        image_data[i + 2] = 0  # blue
        image_data[i + 3] = 0  # alpha

    return image_data


@time_fn
def main() -> None:
    image = create_image(500, 500)


if __name__ == "__main__":
    main()
