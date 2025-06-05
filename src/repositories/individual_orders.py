from src.models.orders import IndividualOrdersModel
from src.utils.repository import SQLAlchemyRepository


class IndividualOrdersRepository(SQLAlchemyRepository):
    model = IndividualOrdersModel