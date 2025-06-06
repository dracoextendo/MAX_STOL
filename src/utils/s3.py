from contextlib import asynccontextmanager
from src.utils.config import s3_config
from aiobotocore.session import get_session
from fastapi import UploadFile

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

    async def upload_to_s3(self, file: UploadFile, file_name: str) -> str:
        async with self.get_client() as s3_client:
            await s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=await file.read()
            )
        return f"{self.domain}/{file_name}"

    async def delete_from_s3(self, key: str) -> None:
        async with self.get_client() as s3_client:
            await s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )

s3client = S3Client(
    access_key=s3_config.access_key.get_secret_value(),
    secret_key=s3_config.secret_key.get_secret_value(),
    endpoint_url=s3_config.endpoint_url.get_secret_value(),
    bucket_name=s3_config.bucket_name.get_secret_value(),
    domain=s3_config.domain.get_secret_value(),
)