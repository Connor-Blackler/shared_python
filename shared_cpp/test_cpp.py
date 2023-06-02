import pytest
from .main import create_image


def test_create_image():
    # Test the creation of an image with the specified width and height
    image_data = create_image(500, 500)
    assert len(image_data) == 500 * 500 * 4
    assert image_data[0] == 255
    assert image_data[1] == 50
    assert image_data[2] == 0
    assert image_data[3] == 0
