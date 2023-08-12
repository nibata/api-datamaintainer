from cryptography.fernet import Fernet
from typing import Any
import json


class Encrypter:
    """
    Class that simplify the encryption and decryption of python object
    """
    def __init__(self, key: bytes):
        self._encrypter = Fernet(key)

    def encrypt(self, obj: Any) -> str:
        """
        Encrypt a python object that can be encoded and dictionaries

        :param obj: Any python object that can be encoded
        :return: str, Encrypted object in string format
        """

        json_obj = json.dumps(obj).encode()
        encrypted_str = self._encrypter.encrypt(json_obj).decode()

        return encrypted_str

    def decrypt(self, encrypted_text: str) -> Any:
        """
        Decrypt the string to a python object

        :param encrypted_text: str, string that can be converted to a python object
        :return: Any object python that can be encoded
        """

        decrypted_json = self._encrypter.decrypt(encrypted_text.encode())

        obj = json.loads(decrypted_json)

        return obj