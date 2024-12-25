from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from config.env import SQLALCHEMY_POSTGRESQL_URL

app = FastAPI()


Base = declarative_base()
engine = create_engine(
	SQLALCHEMY_POSTGRESQL_URL,
	pool_recycle=3600,
	future=True,
	connect_args={'connect_timeout': 30}
)
DBSession = scoped_session(sessionmaker())
DBSession.configure(bind=engine, autoflush=False, expire_on_commit=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
