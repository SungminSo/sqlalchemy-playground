from sqlalchemy import Column, Integer, String, DateTime, Sequence

from playground.models import Base
from playground.utils.time import utcnow


class User(Base):
    # Declarative를 사용한 class는 __tablename__이 반드시 필요
    __tablename__ = 'users'

    # Column(String(50)) 등 컬럼의 길이을 설정하는 것은 SQLite나 PostgreSQL은 상관없지만 기타 다른 데이터베이스를 사용할 때는 필요
    # Sequence는 Firebird나 오라클 등 다른 데이터베이스에서 PK 생성할 때 필요할 수 있음
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    nickname = Column(String(50), nullable=False)
    password = Column(String(200), nullable=False)
    phone = Column(String(15), nullable=False, unique=True)
    created_on = Column(DateTime, default=utcnow, index=True)
    updated_on = Column(DateTime, default=utcnow, onupdate=utcnow)

    def __init__(self, name, nickname, password, phone):
        self.name = name
        self.nickname = nickname
        self.password = password
        self.phone = phone

    def __repr__(self):
        return f"<User(name={self.name}, nickname={self.nickname})>"
