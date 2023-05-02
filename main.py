"""Testing module for shared_python"""
import webbrowser
from shared_open_ai.image_generator import OpenAiImage

images = OpenAiImage("Image with a dog jumping on a trampoline", 3)

for this_url in images:
    webbrowser.open(this_url)
