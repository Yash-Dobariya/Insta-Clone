from jose import jwt
from datetime import datetime, timedelta
from src.config import Config
from src.utils.error_handel import InstaCloneException
from flask_api import status
import jwt as jwt_error
from flask import request, g
from functools import wraps
from src.user.model import User


def create_access_token(subject: dict, expire_time=timedelta(days=1)):
    expire_time = datetime.utcnow() + expire_time
    data = {**subject, "exp": expire_time}
    return jwt.encode(data, key=Config.JWT_SECRET_KEY, algorithm="HS256")


def create_refresh_token(subject: dict, expire_time=timedelta(days=7)):
    expire_time = datetime.utcnow() + expire_time
    data = {**subject, "exp": expire_time}
    return jwt.encode(data, key=Config.JWT_SECRET_KEY, algorithm="HS256")


def token_required(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        try:
            bearer_token = request.headers.get("Authorization")
            token = bearer_token.split()[1]
            payload = jwt.decode(
                token=token, key=Config.JWT_SECRET_KEY, algorithms=["HS256"]
            )
            user = type("MyObject", (object,), payload)
            User.query.filter(
                User.id == user.id,
                User.email_id == user.email_id,
                User.is_delete == False,
            ).first()
            g.user_data = user

            if payload["exp"] >= datetime.timestamp(datetime.now()):
                return f(*args, **kwargs)
            elif jwt_error.exceptions.InvalidSignatureError:
                raise InstaCloneException(
                    message="Invalid token", status_code=status.HTTP_401_UNAUTHORIZED
                )
            else:
                raise InstaCloneException(
                    message="Token is expired", status_code=status.HTTP_401_UNAUTHORIZED
                )
        except jwt_error.exceptions.InvalidTokenError:
            raise InstaCloneException(
                message="Invalid token", status_code=status.HTTP_401_UNAUTHORIZED
            )

    return check_token
