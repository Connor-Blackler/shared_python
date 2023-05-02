import os
import uuid
import webbrowser
import requests
from shared_open_ai.image_generator import OpenAiImage
from shared_face_recognition.main import ImageRecognition

repo = os.getenv('APPDATA') + "\\shared_repo\\FaceRecognition\\"
os.makedirs(repo, mode=777, exist_ok=True)

images_to_process = []
images = OpenAiImage(
    "a man", 1)
for this_image in images:
    webbrowser.open(this_image)
    img_data = requests.get(this_image).content

    image_path = repo + str(uuid.uuid1())
    with open(image_path, "wb") as image:
        image.write(img_data)

    images_to_process.append(image_path)

for this_image_path in images_to_process:
    face_recognition = ImageRecognition(this_image_path)
    print(face_recognition.process())
