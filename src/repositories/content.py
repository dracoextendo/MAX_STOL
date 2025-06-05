from src.models.content import ContentModel
from src.utils.repository import SQLAlchemyRepository


class ContentRepository(SQLAlchemyRepository):
    model = ContentModel