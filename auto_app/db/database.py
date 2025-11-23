from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.engine import create_engine


DB_URL = 'postgresql://postgres:admin@localhost/auction_ii4'


engine = create_engine(DB_URL)


SessionLocale = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass