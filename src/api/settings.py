from fastapi import APIRouter

router = APIRouter(prefix="/settings",tags=['Настройки'])

@router.get('/desk-colors', summary="Получить все цвета столешниц (в разработке)", tags=['Цвет столешницы'])
async def get_all_desk_colors():
    pass

@router.get('/desk-colors/{id}', summary="Получить цвет столешницы по id (в разработке)", tags=['Цвет столешницы'])
async def get_desk_color_by_id():
    pass

@router.post('/desk-colors/{id}', summary="Добавить цвет столешницы (в разработке)", tags=['Цвет столешницы'])
async def add_desk_color_by_id():
    pass

@router.put('/desk-colors/{id}', summary="Изменить цвет столешницы (в разработке)", tags=['Цвет столешницы'])
async def upadte_desk_color_by_id():
    pass

@router.delete('/desk-colors/{id}', summary="Удалить цвет столешницы (в разработке)", tags=['Цвет столешницы'])
async def delete_desk_color_by_id():
    pass

@router.get('/frame-colors', summary="Получить все цвета металлокаркаса (в разработке)", tags=['Цвет металлокаркаса'])
async def get_all_frame_colors():
    pass

@router.get('/frame-colors/{id}', summary="Получить цвет металлокаркаса по id (в разработке)", tags=['Цвет металлокаркаса'])
async def get_frame_color_by_id():
    pass

@router.post('/frame-colors/{id}', summary="Добавить цвет металлокаркаса (в разработке)", tags=['Цвет металлокаркаса'])
async def add_frame_color_by_id():
    pass

@router.put('/frame-colors/{id}', summary="Изменить цвет металлокаркаса (в разработке)", tags=['Цвет металлокаркаса'])
async def upadte_frame_color_by_id():
    pass

@router.delete('/frame-colors/{id}', summary="Удалить цвет металлокаркаса (в разработке)", tags=['Цвет металлокаркаса'])
async def delete_frame_color_by_id():
    pass

@router.get('/lengths', summary="Получить все длины столов (в разработке)", tags=['Длина стола'])
async def get_all_lengths():
    pass

@router.get('/lengths/{id}', summary="Получить длину стола по id (в разработке)", tags=['Длина стола'])
async def get_length_by_id():
    pass

@router.post('/lengths/{id}', summary="Добавить длину стола (в разработке)", tags=['Длина стола'])
async def add_length_by_id():
    pass

@router.put('/lengths/{id}', summary="Изменить длину стола (в разработке)", tags=['Длина стола'])
async def upadte_length_by_id():
    pass

@router.delete('/lengths/{id}', summary="Удалить длину стола (в разработке)", tags=['Длина стола'])
async def delete_length_by_id():
    pass

@router.get('/depths', summary="Получить все глубины столов (в разработке)", tags=['Глубина стола'])
async def get_all_depths():
    pass

@router.get('/depths/{id}', summary="Получить глубину стола по id (в разработке)", tags=['Глубина стола'])
async def get_depth_by_id():
    pass

@router.post('/depths/{id}', summary="Добавить глубину стола (в разработке)", tags=['Глубина стола'])
async def add_depth_by_id():
    pass

@router.put('/depths/{id}', summary="Изменить глубину стола (в разработке)", tags=['Глубина стола'])
async def upadte_depth_by_id():
    pass

@router.delete('/depths/{id}', summary="Удалить глубину стола (в разработке)", tags=['Глубина стола'])
async def delete_depth_by_id():
    pass