from sqlalchemy import Column, Integer, String
from database.db import Base


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    name = Column(String)

    def __repr__(self):
        return "<User(name='%s'," \
               " email='%s'," \
               " password='%s' " % \
               (self.name,
                self.email,
                self.password
                )

    def __init__(self,
                 name: str,
                 email: str,
                 password: str):
        self.name = name
        self.email = email
        self.password = password
