from sqlalchemy import Column, Integer, String, DateTime

from ..models import Base
from ..utils.time import utcnow


class User(Base):
    # Declarative를 사용한 class는 __tablename__이 반드시 필요
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    nickname = Column(String)
    created_on = Column(DateTime, default=utcnow, index=True)
    updated_on = Column(DateTime, default=utcnow, onupdate=utcnow)

    def __repr__(self):
        return f"<User(name={self.name}, nickname={self.nickname})>"
