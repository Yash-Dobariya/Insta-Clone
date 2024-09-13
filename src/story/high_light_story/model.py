from src.utils.same_model import DBmodel
from sqlalchemy import Column, String, JSON, Integer, ForeignKey
from src.user.model import User
from src.database import db
import uuid


def default_uuid():
    return str(uuid.uuid4())


class HighLightStory(db.Model, DBmodel):

    """HighLight story model"""

    __tablename__ = "highlight_story"

    id = Column(String, default=default_uuid, primary_key=True)
    add_highlight = Column(String)
    highlight_type = Column(String)
    uploaded_by = Column(ForeignKey(User.id))
    story_id = Column(String)
    liked_by = Column(JSON, default=[])
    count_like = Column(Integer, default=0)
