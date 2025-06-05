from src.utils.repository import AbstractRepository


class ContentService:
    def __init__(self, content_repository: type[AbstractRepository]):
        self.content_repository: AbstractRepository = content_repository()

    async def get_content(self):
        content = await self.content_repository.get_first()
        return content