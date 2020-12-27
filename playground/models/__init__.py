from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from playground.settings.base import DATABASE

_engine = None


def create_db_engine():
    global _engine

    if _engine is None:
        opts = {'echo': DATABASE['echo']}
        _engine = create_engine(DATABASE['engine'], **opts)
        # echo : SQLAlchemy logging flag
        # lazy connecting : create_engine의 return은 db와의 실제 연결이 아니다. 첫 액션(쿼리 등) 수행 시 db와 실제 연결됨

    return _engine


engine = create_db_engine()

Base = declarative_base()
# sqlalchemy에서는 Declarative를 이용해서 사용할 class를 생성하고 db table에 매핑한다.


Session = sessionmaker(bind=engine)
# engine이 아직 존재하지 않을 경우
# Session = sessionmaker()
# engine 생성 이후
# Session.configure(bind=engine)
