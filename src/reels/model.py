from src.database import db
from sqlalchemy import Column, String, Integer, ForeignKey, JSON
from src.utils.same_model import DBmodel
from src.user.model import User
import uuid


def default_uuid():
    return str(uuid.uuid4())


class ReelsPost(db.Model, DBmodel):

    """reels model"""

    __tablename__ = "reels_post"

    id = Column(String, default=default_uuid, primary_key=True)
    reel_file = Column(String)
    caption = Column(String)
    uploaded_by = Column(ForeignKey(User.id))
    count_like = Column(Integer, default=0)
    liked_by = Column(JSON, default=[])
    comment = Column(JSON, default=[])
    location = Column(String)
