from contextlib import asynccontextmanager
from uuid import uuid4
from config import S3Config
from aiobotocore.session import get_session
from fastapi import UploadFile
from pydantic_settings import SettingsConfigDict


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
            domain: str
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.domain = domain
        self.endpoint_url = endpoint_url
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_to_s3(self, file: UploadFile) -> str:
        file_extension = file.filename.split('.')[-1]
        file_name = f"{uuid4()}.{file_extension}"
        async with self.get_client() as s3_client:
            await s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=await file.read()
            )
        return f"{self.domain}/{file_name}"

config = S3Config()
s3client = S3Client(
    access_key=config.access_key.get_secret_value(),
    secret_key=config.secret_key.get_secret_value(),
    endpoint_url=config.endpoint_url.get_secret_value(),
    bucket_name=config.bucket_name.get_secret_value(),
    domain=config.domain.get_secret_value(),
)