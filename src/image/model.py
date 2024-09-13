from src.database import db
from sqlalchemy import Column, String, ForeignKey, Integer, JSON
import uuid
from src.utils.same_model import DBmodel
from src.user.model import User
import uuid


def default_uuid():
    return str(uuid.uuid4())


class ImagePost(db.Model, DBmodel):

    """image model"""

    __tablename__ = "image_post"

    id = Column(String, default=default_uuid, primary_key=True)
    img_filename = Column(String)
    caption = Column(String)
    uploaded_by = Column(ForeignKey(User.id))
    count_like = Column(Integer, default=0)
    liked_by = Column(JSON, default=[])
    comment = Column(JSON, default=[])
    location = Column(String)
