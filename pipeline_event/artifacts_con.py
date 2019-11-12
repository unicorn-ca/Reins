
from pipeline_event.artifacts import Artifacts as ArtifactsInt
import boto3
import botocore

from typing import BinaryIO

from boto3.session import Session

from boto3_type_annotations import s3


class Artifacts(ArtifactsInt):

    def __init__(self, artifact: dict, cred: dict = {}, encrypt: dict = {}):
        self.name: str = ""
        self.revision: str = ""
        self.type: str = ""
        self.secret_access_key: str = ""
        self.session_token: str = ""
        self.key_id: str = ""
        self.bucket_name: str = ""
        self.file_name: str = ""
        self.encrypt_type: str = ""
        self.encrypt_id: str = ""
        self.s3_client: s3.Client = None
        self.__convert(artifact, cred, encrypt)

    def get_name(self):
        return self.name

    def get_revision(self):
        return self.revision

    def get_type(self):
        return self.type

    def get_cred_secret_access_key(self):
        return self.secret_access_key

    def get_cred_session_token(self):
        return self.session_token

    def get_cred_key_id(self):
        return self.key_id

    def get_bucket_name(self):
        return self.bucket_name

    def get_file_name(self):
        return self.file_name

    def get_encrypt_id(self):
        return self.encrypt_id

    def get_encrypt_type(self):
        return self.encrypt_type

    def set_name(self,item):
        self.name = item

    def set_revision(self,item):
        self.revision = item

    def set_type(self,item):
        self.type = item

    def set_cred_secret_access_key(self,item):
        self.secret_access_key = item

    def set_cred_session_token(self,item):
        self.session_token = item

    def set_cred_key_id(self,item):
        self.key_id = item

    def set_bucket_name(self,item):
        self.bucket_name = item

    def set_file_name(self,item):
        self.file_name = item

    def set_encrypt_id(self, item):
        self.encrypt_id = item

    def set_encrypt_type(self, item):
        self.encrypt_type = item

    def __get_s3_client(self):
        return self.s3_client

    def __set_s3_client(self, item):
        self.s3_client = item

    def __create_s3_client(self) -> s3.Client:
        if self.__get_s3_client():
            session = Session(
                aws_access_key_id=self.get_cred_key_id(),
                aws_session_token=self.get_cred_session_token(),
                aws_secret_access_key=self.get_cred_secret_access_key()
            )
            self.__set_s3_client(session.client('s3', config=botocore.client.Config(signature_version='s3v4')))
        return self.__get_s3_client()

    def upload(self, file: BinaryIO, filename=""):
        if filename == "":
            filename = self.get_file_name()
        s3_client = self.__create_s3_client()
        s3_client.upload_fileobj(file, self.get_bucket_name(), filename)

    def download(self, file: BinaryIO, filename=""):
        if filename == "":
            filename = self.get_file_name()
        s3_client = self.__create_s3_client()
        s3_client.download_fileobj(file, self.get_bucket_name(), filename)

    # Copy From an artifact to self
    def copy_from(self, artifact: 'Artifacts', filename=""):
        with open('temp', 'wb') as data:
            artifact.download(data, filename=filename)
            self.upload(data, filename=filename)

    def copy_to(self, artifact: 'Artifacts', filename=""):
        with open('temp', 'wb') as data:
            self.download(data, filename=filename)
            artifact.upload(data, filename=filename)

    def __convert(self, artifact: dict, cred: dict = {}, encrypt: dict = {}):
        for name, item in artifact.items():
            if "location" == name:
                # Location Info
                for location_name, location_item in item.items():
                    if "s3Location" == location_name:
                        for s3_location_name, s3_location_item in location_item.items():
                            if s3_location_name == "bucketName":
                                self.set_bucket_name(s3_location_item)
                            if s3_location_name == "objectKey":
                                self.set_file_name(s3_location_item)
                    if "type" == location_item:
                        self.set_type(location_item)
            if "revision" == name:
                self.set_revision(item)
            if "name" == name:
                self.set_name(item)

        for name, item in cred.items():
            if name == "secretAccessKey":
                self.set_cred_secret_access_key(item)
            if name == "sessionToken":
                self.set_cred_session_token(item)
            if name == "accessKeyId":
                self.set_cred_key_id(item)

        for name, item in encrypt.items():
            if name == "id":
                self.set_encrypt_id(item)
            if name == "type":
                self.set_encrypt_type(item)


