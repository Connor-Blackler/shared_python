from shared_cpp.main import main
from shared_decorators.main import time_fn
from PIL import Image


@time_fn
def test_image() -> None:
    width = 500
    height = 500

    img = Image.new(mode="RGB", size=(width, height))

    pixels = img.load()
    for i in range(width):
        for j in range(height):
            pixels[i, j] = (255, 50, 0)


main()
test_image()
