from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# use in-memory-only SQLite db
engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/playground', echo=True)
# echo : SQLAlchemy logging flag
# lazy connecting : create_engine의 return은 db와의 실제 연결이 아니다. 첫 액션(쿼리 등) 수행 시 db와 실제 연결됨


Base = declarative_base()
# sqlalchemy에서는 Declarative를 이용해서 사용할 class를 생성하고 db table에 매핑한다.


Session = sessionmaker(bind=engine)
# engine이 아직 존재하지 않을 경우
# Session = sessionmake()
# engine 생성 이후
# Session.configure(bind=engine)
