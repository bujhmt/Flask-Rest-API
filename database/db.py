from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config

Base = declarative_base()
engine = create_engine(f'postgresql://{Config.db_user}:{Config.db_passwd}@{Config.db_url}/{Config.db_name}')
session = sessionmaker(bind=engine)()

def recreate_database():
    print('Recreating database...')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)