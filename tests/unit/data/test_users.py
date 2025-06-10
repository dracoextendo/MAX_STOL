import pytest
from sqlalchemy import select
from src.models.users import UsersModel
from src.schemas.users import SUserIn, SUserOut, SUserPasswordOut
from sqlalchemy.exc import IntegrityError, InvalidRequestError


async def create_users(sessionmaker) -> list[SUserPasswordOut]:
    test_users_models = [UsersModel(id=1,
                                     username="username_1",
                                     email="test1@test.ru",
                                     hashed_password="hash1",
                                      ),
                          UsersModel(id=2,
                                     username="username_2",
                                     email="test2@test.ru",
                                     hashed_password="hash2",
                                     ),
                          UsersModel(id=3,
                                     username="username_3",
                                     email="test3@test.ru",
                                     hashed_password="hash3",
                                     ),
                          ]
    async with sessionmaker() as session:
        for user in test_users_models:
            session.add(user)
        await session.commit()
    test_users_schemas = [model.to_read_password_model() for model in test_users_models]
    return test_users_schemas


class TestUsersGetOne:
    @pytest.mark.asyncio
    async def test_get_one(self, users_repository, sessionmaker):
        users_out = await create_users(sessionmaker)
        result = await users_repository.get_one(id=1)
        assert result is not None
        assert SUserOut.model_validate(result)
        assert result == SUserOut(**users_out[0].model_dump())

    @pytest.mark.asyncio
    async def test_get_one_not_existing(self, users_repository):
        result = await users_repository.get_one(id=-1)
        assert result is None

    @pytest.mark.asyncio
    async def test_get_one_by_username(self, users_repository, sessionmaker):
        users_out = await create_users(sessionmaker)
        result = await users_repository.get_one_by_username(username="username_1")
        assert result is not None
        assert SUserPasswordOut.model_validate(result)
        assert result == users_out[0]

    @pytest.mark.asyncio
    async def test_get_one_by_username_not_existing(self, users_repository):
        result = await users_repository.get_one_by_username(username="username_10")
        assert result is None