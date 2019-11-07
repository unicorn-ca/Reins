from abc import ABC, abstractmethod
from typing import BinaryIO

class Artifacts(ABC):


    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_bucket_name(self):
        pass

    @abstractmethod
    def get_file_name(self):
        pass

    @abstractmethod
    def get_revision(self):
        pass

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def get_cred_secret_access_key(self):
        pass

    @abstractmethod
    def get_cred_session_token(self):
        pass

    @abstractmethod
    def get_cred_key_id(self):
        pass

    @abstractmethod
    def get_encrypt_id(self):
        pass

    @abstractmethod
    def get_encrypt_type(self):
        pass

    @abstractmethod
    def set_name(self, item):
        pass

    @abstractmethod
    def set_revision(self, item):
        pass

    @abstractmethod
    def set_type(self, item):
        pass

    @abstractmethod
    def set_cred_secret_access_key(self, item):
        pass

    @abstractmethod
    def set_cred_session_token(self, item):
        pass

    @abstractmethod
    def set_cred_key_id(self, item):
        pass

    @abstractmethod
    def set_bucket_name(self, item):
        pass

    @abstractmethod
    def set_file_name(self, item):
        pass

    @abstractmethod
    def set_encrypt_id(self, item):
        pass

    @abstractmethod
    def set_encrypt_type(self, item):
        pass

    @abstractmethod
    def download(self, file: BinaryIO):
        pass

    @abstractmethod
    def upload(self, file: BinaryIO):
        pass
