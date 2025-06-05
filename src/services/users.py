

from src.utils.repository import AbstractRepository


class UsersService:
    def __init__(self, users_repository: type[AbstractRepository]):
        self.users_repository: AbstractRepository = users_repository()

    async def get_user(self, id: int):
        user = await self.users_repository.get_one(id)
        return user

    async def get_user_by_username(self, username: str):
        user = await self.users_repository.get_one_by_username(username)
        return user