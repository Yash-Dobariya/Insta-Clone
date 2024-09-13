from sqlalchemy import Column, DateTime, String, Boolean
from datetime import datetime


class DBmodel:

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())
    updated_by = Column(String)
    is_active = Column(Boolean, default=True)
    is_delete = Column(Boolean, default=False)
