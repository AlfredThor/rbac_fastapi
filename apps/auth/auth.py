from apps.auth import router


@router.get('/list', summary='查看')
async def list():

    return {'code': 200, 'list': []}