from src.database import db
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.dialects.postgresql import JSON
import uuid
from src.user.model import User
from datetime import datetime
import uuid

def default_uuid():
    return str(uuid.uuid4())


class Story(db.Model):

    """Story model"""

    __tablename__ = "story"

    id = Column(String, default=default_uuid, primary_key=True)
    add_story = Column(String)
    uploaded_by = Column(ForeignKey(User.id))
    count_like = Column(Integer, default=0)
    liked_by = Column(JSON, default=[])
    comment = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow())


class StoryStageMode(db.Model):

    """story stage_mode model"""

    __tablename__ = "story_stage_mode"

    id = Column(String(), default=default_uuid, primary_key=True)
    user_story = Column(String())
    story_id = Column(String())
    uploaded_by = Column(ForeignKey(User.id))
    liked_by = Column(JSON, default=[])
    count_like = Column(Integer, default=0)
