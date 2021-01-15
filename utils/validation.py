from email.utils import parseaddr
import hashlib
from config import Config


def getHash(password: str):
    return str(hashlib.pbkdf2_hmac('sha256',
                               password.encode('utf-8'),
                               Config.salt.encode('utf-8'),
                               100000,
                               dklen=128))


def checkHash(password: str, password_hash: str):
    return str(hashlib.pbkdf2_hmac('sha256',
                               password.encode('utf-8'),
                               Config.salt.encode('utf-8'),
                               100000,
                               dklen=128)) == password_hash


def isEmailValid(email: str):
    return '@' in parseaddr(email)[1]

