import openai
from .get_api_key import OpenAIApiKey

openai.api_key = OpenAIApiKey().get_api_key()


class OpenAiImage():
    """
    A class that communicates with the OpenAI API.
    Iterable object that iterates number_of_images times
    """

    def __init__(self, image_description: str, number_of_images: int) -> None:
        self.__iter = 0
        self._result = []

        response = openai.Image.create(
            prompt=image_description,
            n=number_of_images,
            size="1024x1024"
        )

        for i in range(0, number_of_images):
            self._result.append(response['data'][i]["url"])

    def __iter__(self):
        self.__iter = 0
        return self

    def __next__(self):
        if self.__iter >= len(self._result):
            del self.__iter
            raise StopIteration
        else:
            ret = self._result[self.__iter]
            self.__iter += 1
            return ret
