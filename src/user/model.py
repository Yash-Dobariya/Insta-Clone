from src.database import db
from sqlalchemy import Column, String, Date
from src.utils.same_model import DBmodel
import uuid


def default_uuid():
    return str(uuid.uuid4())


class User(db.Model, DBmodel):

    """user model"""

    __tablename__ = "user"

    id = Column(String, default=default_uuid, primary_key=True)
    user_name = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email_id = Column(String, unique=True)
    password = Column(String)
    dob = Column(Date)
    country = Column(String)
    bio = Column(String)
