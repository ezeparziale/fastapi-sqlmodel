from sqlmodel import Session, create_engine

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI.unicode_string())

SessionLocal = Session(autocommit=False, autoflush=False, bind=engine)


def get_db():

    with Session(autocommit=False, autoflush=False, bind=engine) as session:
        yield session
