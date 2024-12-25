from config.config import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    # except Exception as error:
    #     db.rollback()
    #     logger.error(f'get_db报错! 报错信息: {error}')
    #     print('get_db报错:', error)
    #     raise HTTPException(status_code=500, detail=error.__dict__.get('detail'))
    finally:
        db.close()
