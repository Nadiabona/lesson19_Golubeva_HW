import hashlib
import base64, hmac

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self):
        return self.dao.get_all()

    def get_by_email(self, email):
        return self.dao.get_by_email(email)

    def create(self, user_d):
        user_d["password"] = self.make_password_hash(user_d.get("password"))
        return self.dao.create(user_d)

    def update(self, user_d):
        self.dao.update(user_d)
        return self.dao

    def delete(self, rid):
        self.dao.delete(rid)

    def make_password_hash(self, password):    #пароль, который вводит пользователь при регистрации
        return base64.b64encode(hashlib.pbkdf2_hmac( #чтобы русские буквы переваривал
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS))
            #.decode("utf-8", "ignore") - сначало не нужен

    #метод сравнения паролей - захешированного и того, что в базе
    def compare_password(self, password_hash, request_password):
        return hmac.compare_digest(
            base64.b64decode(password_hash),
            hashlib.pbkdf2_hmac('sha256',
                                request_password.encode('utf-8'),  # Convert the password to bytes
                                PWD_HASH_SALT,
                                PWD_HASH_ITERATIONS)
                            )#сравниваем посимвольно строчку ascii