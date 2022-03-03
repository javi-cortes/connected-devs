from sqlalchemy import Column, Integer, DateTime, func, Boolean, String, ARRAY

from app.db.base_class import Base


class RequestRegister(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    dev1 = Column(String, index=True)
    dev2 = Column(String, index=True)
    connected = Column(Boolean)
    organizations = Column(ARRAY(String))
