from uuid import uuid4
from fastapi import UploadFile
from src.utils.s3 import s3client, S3Client


class S3Service:
    def __init__(self, client: S3Client = s3client):
        self.client = client

    async def upload_file(self, file: UploadFile):
        file_extension = file.filename.split('.')[-1]
        file_name = f"{uuid4()}.{file_extension}"
        await self.client.upload_to_s3(file, file_name)
        return f"{self.client.domain}/{file_name}"

    async def delete_file(self, url: str) -> None:
        key = url.replace(f"{self.client.domain}/", "")
        await self.client.delete_from_s3(key)


