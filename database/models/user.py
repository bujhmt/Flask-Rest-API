from sqlalchemy import Column, Integer, String
from database.db import Base, session
from utils.validation import checkHash, isEmailValid, getHash
from sqlalchemy.orm import validates


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)

    def setPassword(self, password: str):
        if not password:
            raise AssertionError('Password not provided')
        if len(password) < 6 or len(password) > 50:
            raise AssertionError('Password must be between 6 and 50 characters')
        self.password_hash = getHash(password)

    def checkPassword(self, password: str):
        return checkHash(password, self.password_hash)

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('No email provided')
        if not isEmailValid(email):
            raise AssertionError('Provided email is not an email address')
        if session.query(User).filter(User.email == email).first():
            raise AssertionError('This email is already in use')

        return email
