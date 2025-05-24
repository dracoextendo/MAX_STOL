from typing import Annotated
from fastapi import APIRouter, HTTPException, Form, Depends, status
from src.api.dependencies import access_token_validation
from src.api.responses import UNAUTHORIZED, FORBIDDEN, NOT_FOUND
from src.dao.dao import FrameColorDAO, DeskColorDAO, LengthDAO, DepthDAO
from src.models.products import FrameColors, DeskColors, Length, Depth
from src.schemas.base import SStatusOut
from src.schemas.settings import SDeskColorOut, SFrameColorOut, SLengthOut, SDepthOut, SDeskColorIn, SFrameColorIn, \
    SLengthIn, SDepthIn

router = APIRouter(prefix="/settings",
                   dependencies=[Depends(access_token_validation)],
                   responses ={**UNAUTHORIZED, **FORBIDDEN},)

@router.get('/desk-colors',
            summary="Получить все цвета столешниц",
            tags=['Цвет столешницы'],
            response_model=list[SDeskColorOut])
async def get_all_desk_colors():
    return await DeskColorDAO.find_all()

@router.get('/desk-colors/{id}',
            summary="Получить цвет столешницы по id",
            tags=['Цвет столешницы'],
            responses ={**NOT_FOUND},
            response_model=SDeskColorOut)
async def get_desk_color_by_id(id: int):
    result = await DeskColorDAO.get_desk_color(id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Desk color id = {id} not found")
    return result

@router.post('/desk-colors/add',
             summary="Добавить цвет столешницы",
             tags=['Цвет столешницы'],
             response_model=SStatusOut,
             status_code=status.HTTP_201_CREATED)
async def add_desk_color(color: SDeskColorIn = Depends(SDeskColorIn.as_form)):
    desk_color = DeskColors(
        name=color.name,
        sort=color.sort,
    )
    return await DeskColorDAO.add_desk_color(desk_color)

@router.put('/desk-colors/{id}',
            summary="Изменить цвет столешницы",
            tags=['Цвет столешницы'],
            responses ={**NOT_FOUND},
            response_model=SStatusOut)
async def update_desk_color_by_id(id: int, color: SDeskColorIn = Depends(SDeskColorIn.as_form)):
    desk_color = DeskColors(
        name=color.name,
        sort=color.sort,
    )
    return await DeskColorDAO.update_desk_color(id, desk_color)

@router.delete('/desk-colors/{id}',
               summary="Удалить цвет столешницы",
               tags=['Цвет столешницы'],
               responses ={**NOT_FOUND},
               response_model=SStatusOut)
async def delete_desk_color_by_id(id: int):
    return await DeskColorDAO.delete_desk_color(id)

@router.get('/frame-colors',
            summary="Получить все цвета металлокаркаса",
            tags=['Цвет металлокаркаса'],
            response_model=list[SFrameColorOut])
async def get_all_frame_colors():
    return await FrameColorDAO.find_all()

@router.get('/frame-colors/{id}',
            summary="Получить цвет металлокаркаса по id",
            tags=['Цвет металлокаркаса'],
            responses ={**NOT_FOUND},
            response_model=SFrameColorOut)
async def get_frame_color_by_id(id: int):
    result = await FrameColorDAO.get_frame_color(id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Frame color id = {id} not found")
    return result

@router.post('/frame-colors/add',
             summary="Добавить цвет металлокаркаса",
             tags=['Цвет металлокаркаса'],
             responses ={**NOT_FOUND},
             response_model=SStatusOut,
             status_code=status.HTTP_201_CREATED)
async def add_frame_color(color: SFrameColorIn = Depends(SFrameColorIn.as_form)):
    frame_color = FrameColors(
        name=color.name,
        sort=color.sort,
    )
    return await FrameColorDAO.add_frame_color(frame_color)

@router.put('/frame-colors/{id}',
            summary="Изменить цвет металлокаркаса",
            tags=['Цвет металлокаркаса'],
            responses ={**NOT_FOUND},
            response_model=SStatusOut)
async def update_frame_color_by_id(id: int, color: SFrameColorIn = Depends(SFrameColorIn.as_form)):
    frame_color = FrameColors(
        name=color.name,
        sort=color.sort,
    )
    return await FrameColorDAO.update_frame_color(id, frame_color)

@router.delete('/frame-colors/{id}',
               summary="Удалить цвет металлокаркаса",
               tags=['Цвет металлокаркаса'],
               responses ={**NOT_FOUND},
               response_model=SStatusOut)
async def delete_frame_color_by_id(id: int):
    return await FrameColorDAO.delete_frame_color(id)

@router.get('/lengths',
            summary="Получить все длины столов",
            tags=['Длина стола'],
            response_model=list[SLengthOut])
async def get_all_lengths():
    return await LengthDAO.find_all()

@router.get('/lengths/{id}',
            summary="Получить длину стола по id",
            tags=['Длина стола'],
            responses ={**NOT_FOUND},
            response_model=SLengthOut)
async def get_length_by_id(id: int):
    result = await LengthDAO.get_length(id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Length id = {id} not found")
    return result

@router.post('/lengths/add',
             summary="Добавить длину стола",
             tags=['Длина стола'],
             response_model=SStatusOut,
             status_code=status.HTTP_201_CREATED)
async def add_length_by_id(length: SLengthIn = Depends(SLengthIn.as_form)):
    length = Length(
        value=length.value,
        sort=length.sort,
    )
    return await LengthDAO.add_length(length)

@router.put('/lengths/{id}',
            summary="Изменить длину стола",
            tags=['Длина стола'],
            responses ={**NOT_FOUND},
            response_model=SStatusOut)
async def update_length_by_id(id: int, length: SLengthIn = Depends(SLengthIn.as_form)):
    length = Length(
        value=length.value,
        sort=length.sort,
    )
    return await LengthDAO.update_length(id, length)

@router.delete('/lengths/{id}',
               summary="Удалить длину стола",
               tags=['Длина стола'],
               responses ={**NOT_FOUND},
               response_model=SStatusOut)
async def delete_length_by_id(id: int):
    return await LengthDAO.delete_length(id)

@router.get('/depths',
            summary="Получить все глубины столов",
            tags=['Глубина стола'],
            response_model=list[SDepthOut])
async def get_all_depths():
    return await DepthDAO.find_all()

@router.get('/depths/{id}',
            summary="Получить глубину стола по id",
            tags=['Глубина стола'],
            responses ={**NOT_FOUND},
            response_model=SDepthOut)
async def get_depth_by_id(id: int):
    result = await DepthDAO.get_depth(id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Depth id = {id} not found")
    return result

@router.post('/depths/add',
             summary="Добавить глубину стола",
             tags=['Глубина стола'],
             response_model=SStatusOut,
             status_code=status.HTTP_201_CREATED)
async def add_depth_by_id(depth: SDepthIn = Depends(SDepthIn.as_form)):
    depth = Depth(
        value=depth.value,
        sort=depth.sort,
    )
    return await DepthDAO.add_depth(depth)


@router.put('/depths/{id}',
            summary="Изменить глубину стола",
            tags=['Глубина стола'],
            responses ={**NOT_FOUND},
            response_model=SStatusOut)
async def update_depth_by_id(id: int, depth: SDepthIn = Depends(SDepthIn.as_form)):
    depth = Depth(
        value=depth.value,
        sort=depth.sort,
    )
    return await DepthDAO.update_depth(id, depth)

@router.delete('/depths/{id}',
               summary="Удалить глубину стола",
               tags=['Глубина стола'],
               responses ={**NOT_FOUND},
               response_model=SStatusOut)
async def delete_depth_by_id(id: int):
    return await DepthDAO.delete_depth(id)