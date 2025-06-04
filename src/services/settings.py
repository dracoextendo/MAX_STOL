from src.schemas.settings import SDeskColorIn, SFrameColorIn, SDepthIn, SLengthIn
from src.utils.repository import AbstractRepository


class SettingsService:
    def __init__(self, settings_repository: type[AbstractRepository]):
        self.settings_repository: AbstractRepository = settings_repository()

    async def get_parameter(self, id: int):
        param = await self.settings_repository.get_one(id)
        return param

    async def add_parameter(self, param: SDeskColorIn | SFrameColorIn | SDepthIn | SLengthIn):
        param_dict = param.model_dump()
        param_id = await self.settings_repository.add_one(param_dict)
        return param_id

    async def update_parameter(self, id: int, param: SDeskColorIn | SFrameColorIn | SDepthIn | SLengthIn) -> int:
        param_dict = param.model_dump()
        param_id = await self.settings_repository.update_one(id, param_dict)
        return param_id

    async def delete_parameter(self, id: int):
        param_id = await self.settings_repository.delete_one(id)
        return param_id

    async def get_all_parameters(self):
        parameters = await self.settings_repository.get_all(order_by = ["sort", "id"])
        return parameters