from fastapi import APIRouter, HTTPException, Depends, status, Response, Request
from src.api.dependencies import desk_color_service, frame_color_service, length_service, \
    depth_service, auth_service
from src.utils.responses import UNAUTHORIZED, NOT_FOUND
from src.schemas.base import SStatusOut
from src.schemas.desk_settings import SDeskColorOut, SFrameColorOut, SLengthOut, SDepthOut, SDeskColorIn, SFrameColorIn, \
    SLengthIn, SDepthIn
from src.services.auth import AuthService
from src.services.desk_settings import SettingsService
from src.utils.config import SECURE_COOKIE

router = APIRouter(prefix="/settings",
                   responses ={**UNAUTHORIZED},)

@router.get('/desk-colors',
            summary="Получить все цвета столешниц",
            tags=['Цвет столешницы'],
            response_model=list[SDeskColorOut])
async def get_all_desk_colors(request: Request,
                              response: Response,
                              service: SettingsService = Depends(desk_color_service),
                              auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    desk_colors = await service.get_all_parameters()
    if not desk_colors:
        raise HTTPException(status_code=404, detail="Desk colors not found")
    return desk_colors

@router.get('/desk-colors/{id}',
            summary="Получить цвет столешницы по id",
            tags=['Цвет столешницы'],
            responses ={**NOT_FOUND},
            response_model=SDeskColorOut)
async def get_desk_color_by_id(request: Request,
                               response: Response,
                               id: int,
                               service: SettingsService = Depends(desk_color_service),
                               auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    desk_color = await service.get_parameter(id)
    if not desk_color:
        raise HTTPException(status_code=404, detail="Desk color not found")
    return desk_color

@router.post('/desk-colors/add',
             summary="Добавить цвет столешницы",
             tags=['Цвет столешницы'],
             response_model=SStatusOut,
             status_code=status.HTTP_201_CREATED)
async def add_desk_color(request: Request,
                         response: Response,
                         color: SDeskColorIn = Depends(SDeskColorIn.as_form),
                         service: SettingsService = Depends(desk_color_service),
                         auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    desk_color_id = await service.add_parameter(color)
    return SStatusOut(detail=f"desk color id = {desk_color_id} added")

@router.put('/desk-colors/{id}',
            summary="Изменить цвет столешницы",
            tags=['Цвет столешницы'],
            responses ={**NOT_FOUND},
            response_model=SStatusOut)
async def update_desk_color_by_id(request: Request,
                                  response: Response,
                                  id: int, color: SDeskColorIn = Depends(SDeskColorIn.as_form),
                                  service: SettingsService = Depends(desk_color_service),
                                  auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    desk_color_id = await service.update_parameter(id, color)
    if not desk_color_id:
        raise HTTPException(status_code=404, detail="Desk color not found")
    return SStatusOut(detail=f"desk color id = {desk_color_id} updated")

@router.delete('/desk-colors/{id}',
               summary="Удалить цвет столешницы",
               tags=['Цвет столешницы'],
               responses ={**NOT_FOUND},
               response_model=SStatusOut)
async def delete_desk_color_by_id(request: Request,
                                  response: Response,
                                  id: int, service: SettingsService = Depends(desk_color_service),
                                  auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    desk_color_id = await service.delete_parameter(id)
    if not desk_color_id:
        raise HTTPException(status_code=404, detail="Desk color not found")
    return SStatusOut(detail=f"desk color id = {desk_color_id} deleted")

@router.get('/frame-colors',
            summary="Получить все цвета металлокаркаса",
            tags=['Цвет металлокаркаса'],
            response_model=list[SFrameColorOut])
async def get_all_frame_colors(request: Request,
                               response: Response,
                               service: SettingsService = Depends(frame_color_service),
                               auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    frame_colors = await service.get_all_parameters()
    if not frame_colors:
        raise HTTPException(status_code=404, detail="Frame colors not found")
    return frame_colors

@router.get('/frame-colors/{id}',
            summary="Получить цвет металлокаркаса по id",
            tags=['Цвет металлокаркаса'],
            responses ={**NOT_FOUND},
            response_model=SFrameColorOut)
async def get_frame_color_by_id(request: Request,
                                response: Response,
                                id: int, service: SettingsService = Depends(frame_color_service),
                                auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    frame_color = await service.get_parameter(id)
    if not frame_color:
        raise HTTPException(status_code=404, detail="Frame color not found")
    return frame_color

@router.post('/frame-colors/add',
             summary="Добавить цвет металлокаркаса",
             tags=['Цвет металлокаркаса'],
             responses ={**NOT_FOUND},
             response_model=SStatusOut,
             status_code=status.HTTP_201_CREATED)
async def add_frame_color(request: Request,
                          response: Response,
                          color: SFrameColorIn = Depends(SFrameColorIn.as_form),
                          service: SettingsService = Depends(frame_color_service),
                          auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    frame_color_id = await service.add_parameter(color)
    return SStatusOut(detail=f"frame color id = {frame_color_id} added")

@router.put('/frame-colors/{id}',
            summary="Изменить цвет металлокаркаса",
            tags=['Цвет металлокаркаса'],
            responses ={**NOT_FOUND},
            response_model=SStatusOut)
async def update_frame_color_by_id(request: Request,
                                   response: Response,
                                   id: int,
                                   color: SFrameColorIn = Depends(SFrameColorIn.as_form),
                                   service: SettingsService = Depends(frame_color_service),
                                   auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    frame_color_id = await service.update_parameter(id, color)
    if not frame_color_id:
        raise HTTPException(status_code=404, detail="Frame color not found")
    return SStatusOut(detail=f"frame color id = {frame_color_id} updated")

@router.delete('/frame-colors/{id}',
               summary="Удалить цвет металлокаркаса",
               tags=['Цвет металлокаркаса'],
               responses ={**NOT_FOUND},
               response_model=SStatusOut)
async def delete_frame_color_by_id(request: Request,
                                   response: Response,
                                   id: int,
                                   service: SettingsService = Depends(frame_color_service),
                                   auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    frame_color_id = await service.delete_parameter(id)
    if not frame_color_id:
        raise HTTPException(status_code=404, detail="Frame color not found")
    return SStatusOut(detail=f"frame color id = {frame_color_id} deleted")

@router.get('/lengths',
            summary="Получить все длины столов",
            tags=['Длина стола'],
            response_model=list[SLengthOut])
async def get_all_lengths(request: Request,
                          response: Response,
                          auth_service: AuthService = Depends(auth_service),
                          service: SettingsService = Depends(length_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    lengths = await service.get_all_parameters()
    if not lengths:
        raise HTTPException(status_code=404, detail="Lengths not found")
    return lengths

@router.get('/lengths/{id}',
            summary="Получить длину стола по id",
            tags=['Длина стола'],
            responses ={**NOT_FOUND},
            response_model=SLengthOut)
async def get_length_by_id(request: Request,
                           response: Response,
                           id: int,
                           service: SettingsService = Depends(length_service),
                           auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    length = await service.get_parameter(id)
    if not length:
        raise HTTPException(status_code=404, detail="Length not found")
    return length

@router.post('/lengths/add',
             summary="Добавить длину стола",
             tags=['Длина стола'],
             response_model=SStatusOut,
             status_code=status.HTTP_201_CREATED)
async def add_length(request: Request,
                     response: Response,
                     length: SLengthIn = Depends(SLengthIn.as_form),
                     service: SettingsService = Depends(length_service),
                     auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    length_id = await service.add_parameter(length)
    return SStatusOut(detail=f"length id = {length_id} added")

@router.put('/lengths/{id}',
            summary="Изменить длину стола",
            tags=['Длина стола'],
            responses ={**NOT_FOUND},
            response_model=SStatusOut)
async def update_length_by_id(request: Request,
                              response: Response,
                              id: int,
                              length: SLengthIn = Depends(SLengthIn.as_form),
                              service: SettingsService = Depends(length_service),
                              auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    length_id = await service.update_parameter(id, length)
    if not length_id:
        raise HTTPException(status_code=404, detail="Length not found")
    return SStatusOut(detail=f"length id = {length_id} updated")

@router.delete('/lengths/{id}',
               summary="Удалить длину стола",
               tags=['Длина стола'],
               responses ={**NOT_FOUND},
               response_model=SStatusOut)
async def delete_length_by_id(request: Request,
                              response: Response,
                              id: int,
                              service: SettingsService = Depends(length_service),
                              auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    length_id = await service.delete_parameter(id)
    if not length_id:
        raise HTTPException(status_code=404, detail="Length not found")
    return SStatusOut(detail=f"length id = {length_id} deleted")

@router.get('/depths',
            summary="Получить все глубины столов",
            tags=['Глубина стола'],
            response_model=list[SDepthOut])
async def get_all_depths(request: Request,
                         response: Response,
                         service: SettingsService = Depends(depth_service),
                         auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    depths = await service.get_all_parameters()
    if not depths:
        raise HTTPException(status_code=404, detail="Depths not found")
    return depths

@router.get('/depths/{id}',
            summary="Получить глубину стола по id",
            tags=['Глубина стола'],
            responses ={**NOT_FOUND},
            response_model=SDepthOut)
async def get_depth_by_id(request: Request,
                          response: Response,
                          id: int,
                          service: SettingsService = Depends(depth_service),
                          auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    depth = await service.get_parameter(id)
    if not depth:
        raise HTTPException(status_code=404, detail="Depth not found")
    return depth

@router.post('/depths/add',
             summary="Добавить глубину стола",
             tags=['Глубина стола'],
             response_model=SStatusOut,
             status_code=status.HTTP_201_CREATED)
async def add_depth(request: Request,
                    response: Response,
                    depth: SDepthIn = Depends(SDepthIn.as_form),
                    service: SettingsService = Depends(depth_service),
                    auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    depth_id = await service.add_parameter(depth)
    return SStatusOut(detail=f"depth id = {depth_id} added")


@router.put('/depths/{id}',
            summary="Изменить глубину стола",
            tags=['Глубина стола'],
            responses ={**NOT_FOUND},
            response_model=SStatusOut)
async def update_depth_by_id(request: Request,
                             response: Response,
                             id: int,
                             depth: SDepthIn = Depends(SDepthIn.as_form),
                             service: SettingsService = Depends(depth_service),
                             auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    depth_id = await service.update_parameter(id, depth)
    if not depth_id:
        raise HTTPException(status_code=404, detail="Depth not found")
    return SStatusOut(detail=f"depth id = {depth_id} updated")

@router.delete('/depths/{id}',
               summary="Удалить глубину стола",
               tags=['Глубина стола'],
               responses ={**NOT_FOUND},
               response_model=SStatusOut)
async def delete_depth_by_id(request: Request,
                             response: Response,
                             id: int,
                             service: SettingsService = Depends(depth_service),
                             auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    depth_id = await service.delete_parameter(id)
    if not depth_id:
        raise HTTPException(status_code=404, detail="Depth not found")
    return SStatusOut(detail=f"depth id = {depth_id} deleted")