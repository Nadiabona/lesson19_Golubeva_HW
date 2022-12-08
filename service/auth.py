import datetime, calendar
import jwt

from constants import JWT_SECRET, JWT_ALGORITHM
from service.user import UserService

class AuthService:
    def __init__(self, user_service:UserService): #надо чтобы взаимодействовать - получать логин, пароль и генерить токены
        self.user_service = user_service
    def generate_token(self, username, password, is_refresh=False):
        user = self.user_service.get_by_username(username)

        if user is None:
            raise Exception()

        if not is_refresh:
            if not self.user_service.compare_password(user.password, password):
                raise Exception

        data = {
            "username" : user.username,
            "role" : user.role
        }

        access_token_lifetime = datetime.datetime.utcnow() + datetime.timedelta(minutes = 60)
        data["exp"] = calendar.timegm(access_token_lifetime.timetuple()) #timegm приводит формат времени к устоявшемуся, чтобы не слетали кодировки
        access_token =jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        refresh_token_lifetime = datetime.datetime.utcnow() + datetime.timedelta(days=180)
        data["exp"] = calendar.timegm(
        refresh_token_lifetime.timetuple())  # timegm приводит формат времени к устоявшемуся, чтобы не слетали кодировки
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return{"access_token": access_token, "refresh_token" : refresh_token}

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(jwt = refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = data.get("username")

        user = self.user_service.get_by_username(username = username)

        if user is None:
            raise Exception()
        return self.generate_token(username, user.password, is_refresh=True)

    def valid_token(self, access_token, refresh_token):
        for t in [access_token, refresh_token]:
            try:
                jwt.decode(jwt = t, key = JWT_SECRET, algorithms = [JWT_ALGORITHM])
            except Exception as e:
                return True

        return False





