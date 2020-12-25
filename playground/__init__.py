from sqlalchemy import create_engine

# use in-memory-only SQLite db
engine = create_engine('sqlite:///:memory', echo=True)

# echo : SQLAlchemy loggin flag
# lazy connectiong : create_engine의 return은 db와의 실제 연결이 아니다. 첫 액션(쿼리 등) 수행 시 db와 실제 연결됨
