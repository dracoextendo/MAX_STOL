from src.models.products import DeskColors, FrameColors, Depth, Length
from src.utils.repository import SQLAlchemyRepository


class DeskColorsRepository(SQLAlchemyRepository):
    model = DeskColors

class FrameColorsRepository(SQLAlchemyRepository):
    model = FrameColors

class DepthRepository(SQLAlchemyRepository):
    model = Depth

class LengthRepository(SQLAlchemyRepository):
    model = Length
