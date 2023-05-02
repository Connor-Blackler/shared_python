"""Handle the API Key storage used with OpenAI"""

import os
import pickle


class OpenAIApiKey:
    """A class that handles the OpenAI API Key

    This class is repsonsible for storing locally on the harddisk using pickle on a str object
    """

    def __init__(self, cache: bool = True) -> None:
        self.__ensure_api_key_file(cache)

    def __api_folder(self) -> str:
        path = os.getenv('APPDATA')
        return path + "\\shared_repo\\OpenAI"

    def __api_path(self) -> str:
        return self.__api_folder() + "\\API_KEY"

    def __ensure_api_key_file(self, cache: bool) -> None:
        if os.path.exists(self.__api_path()) and not cache:
            os.remove(self.__api_path())

        os.makedirs(self.__api_folder(), mode=777, exist_ok=True)

        try:
            load_file = open(self.__api_path(), "rb")
            ret = pickle.load(load_file)
            load_file.close()

        except FileNotFoundError:
            success = False
            while not success:
                print("Please enter your API Key...")
                ret = input()
                print(f"Type 'y' if this is your API Key: {ret}")
                success = input() == "y"

            load_file = open(self.__api_path(), "wb")
            pickle.dump(ret, load_file)
            load_file.close()

        return ret

    def get_api_key(self) -> str:
        """Method that returns a valid API Key"""
        load_file = open(self.__api_path(), "rb")
        ret = pickle.load(load_file)
        load_file.close()

        return ret
