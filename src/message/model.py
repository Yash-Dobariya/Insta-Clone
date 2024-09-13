from src.database import db
from sqlalchemy import Column, String, ForeignKey, DateTime, String
from src.user.model import User
from datetime import datetime
import uuid


def default_uuid():
    return str(uuid.uuid4())


class Message(db.Model):

    """message model"""

    __tablename__ = "message"

    id = Column(String, default=default_uuid, primary_key=True)
    message = Column(String)
    sender_id = Column(ForeignKey(User.id))
    message_receive = Column(ForeignKey(User.id))
    send_at = Column(DateTime, default=datetime.utcnow())
