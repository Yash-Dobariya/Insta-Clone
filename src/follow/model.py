from src.database import db
from sqlalchemy import Column, ForeignKey, String
from src.user.model import User
from sqlalchemy.orm import relationship
import uuid


def default_uuid():
    return str(uuid.uuid4())


class Follow(db.Model):

    """follow model"""

    __tablename__ = "follow"

    id = Column(String, default=default_uuid, primary_key=True)
    following = Column(String, ForeignKey(User.id))
    follower = Column(String, ForeignKey(User.id))

    user_following = relationship("User", foreign_keys=[following])
    user_follower = relationship("User", foreign_keys=[follower])
