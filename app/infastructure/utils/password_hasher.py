import bcrypt

from application.interfaces import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):

    def hash(self, password: str):
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        hashed: bytes = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed.decode("utf-8")

    def verify(self, password: str, hashed_password: str):
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
