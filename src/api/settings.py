from typing import Annotated
from fastapi import APIRouter, HTTPException, Form, Depends

from src.dao.dao import FrameColorDAO, DeskColorDAO, LengthDAO, DepthDAO
from src.models.products import FrameColors, DeskColors, Length, Depth
from src.security import security

router = APIRouter(prefix="/settings")

@router.get('/desk-colors', dependencies=[Depends(security.access_token_required)], summary="Получить все цвета столешниц", tags=['Цвет столешницы'])
async def get_all_desk_colors():
    return await DeskColorDAO.find_all()

@router.get('/desk-colors/{id}', dependencies=[Depends(security.access_token_required)], summary="Получить цвет столешницы по id", tags=['Цвет столешницы'])
async def get_desk_color_by_id(id: int):
    result = await DeskColorDAO.get_desk_color(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Desk color not found")
    return result

@router.post('/desk-colors/add', dependencies=[Depends(security.access_token_required)], summary="Добавить цвет столешницы", tags=['Цвет столешницы'])
async def add_desk_color(color: Annotated[str, Form()]):
    desk_color = DeskColors(
        name=color
    )
    return await DeskColorDAO.add_desk_color(desk_color)

@router.put('/desk-colors/{id}', dependencies=[Depends(security.access_token_required)], summary="Изменить цвет столешницы", tags=['Цвет столешницы'])
async def upadte_desk_color_by_id(id: int, color: Annotated[str, Form()]):
    desk_color = DeskColors(
        name=color
    )
    return await DeskColorDAO.update_desk_color(id, desk_color)

@router.delete('/desk-colors/{id}', dependencies=[Depends(security.access_token_required)], summary="Удалить цвет столешницы", tags=['Цвет столешницы'])
async def delete_desk_color_by_id(id: int):
    return await DeskColorDAO.delete_desk_color(id)

@router.get('/frame-colors', dependencies=[Depends(security.access_token_required)], summary="Получить все цвета металлокаркаса", tags=['Цвет металлокаркаса'])
async def get_all_frame_colors():
    return await FrameColorDAO.find_all()

@router.get('/frame-colors/{id}', dependencies=[Depends(security.access_token_required)], summary="Получить цвет металлокаркаса по id", tags=['Цвет металлокаркаса'])
async def get_frame_color_by_id(id: int):
    result = await FrameColorDAO.get_frame_color(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Frame color not found")
    return result

@router.post('/frame-colors/add', dependencies=[Depends(security.access_token_required)], summary="Добавить цвет металлокаркаса", tags=['Цвет металлокаркаса'])
async def add_frame_color(color: Annotated[str, Form()]):
    frame_color = FrameColors(
        name=color
    )
    return await FrameColorDAO.add_frame_color(frame_color)

@router.put('/frame-colors/{id}', dependencies=[Depends(security.access_token_required)], summary="Изменить цвет металлокаркаса", tags=['Цвет металлокаркаса'])
async def upadte_frame_color_by_id(id: int, color: Annotated[str, Form()]):
    frame_color = FrameColors(
        name=color
    )
    return await FrameColorDAO.update_frame_color(id, frame_color)

@router.delete('/frame-colors/{id}', dependencies=[Depends(security.access_token_required)], summary="Удалить цвет металлокаркаса", tags=['Цвет металлокаркаса'])
async def delete_frame_color_by_id(id: int):
    return await FrameColorDAO.delete_frame_color(id)

@router.get('/lengths', dependencies=[Depends(security.access_token_required)], summary="Получить все длины столов", tags=['Длина стола'])
async def get_all_lengths():
    return await LengthDAO.find_all()

@router.get('/lengths/{id}', dependencies=[Depends(security.access_token_required)], summary="Получить длину стола по id", tags=['Длина стола'])
async def get_length_by_id(id: int):
    result = await LengthDAO.get_length(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Length not found")
    return result

@router.post('/lengths/add', dependencies=[Depends(security.access_token_required)], summary="Добавить длину стола", tags=['Длина стола'])
async def add_length_by_id(length: Annotated[int, Form()]):
    length = Length(
        value=length
    )
    return await LengthDAO.add_length(length)

@router.put('/lengths/{id}', dependencies=[Depends(security.access_token_required)], summary="Изменить длину стола", tags=['Длина стола'])
async def upadte_length_by_id(id: int, length: Annotated[int, Form()]):
    length = Length(
        value=length
    )
    return await LengthDAO.update_length(id, length)

@router.delete('/lengths/{id}', dependencies=[Depends(security.access_token_required)], summary="Удалить длину стола", tags=['Длина стола'])
async def delete_length_by_id(id: int):
    return await LengthDAO.delete_length(id)

@router.get('/depths', dependencies=[Depends(security.access_token_required)], summary="Получить все глубины столов", tags=['Глубина стола'])
async def get_all_depths():
    return await DepthDAO.find_all()

@router.get('/depths/{id}', dependencies=[Depends(security.access_token_required)], summary="Получить глубину стола по id", tags=['Глубина стола'])
async def get_depth_by_id(id: int):
    result = await DepthDAO.get_depth(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Depth not found")
    return result

@router.post('/depths/add', dependencies=[Depends(security.access_token_required)], summary="Добавить глубину стола", tags=['Глубина стола'])
async def add_depth_by_id(depth: Annotated[int, Form()]):
    depth = Depth(
        value=depth
    )
    return await DepthDAO.add_depth(depth)


@router.put('/depths/{id}', dependencies=[Depends(security.access_token_required)], summary="Изменить глубину стола", tags=['Глубина стола'])
async def upadte_depth_by_id(id: int, depth: Annotated[int, Form()]):
    depth = Depth(
        value=depth
    )
    return await DepthDAO.update_depth(id, depth)

@router.delete('/depths/{id}', dependencies=[Depends(security.access_token_required)], summary="Удалить глубину стола", tags=['Глубина стола'])
async def delete_depth_by_id(id: int):
    return await DepthDAO.delete_depth(id)