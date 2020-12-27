import time

from playground.models.users import User
from playground.utils.database import orm_session


def get_list_query():
    with orm_session() as session:
        # 전체 리스트에서 name, nickname만 출력하는 방법
        # 1
        start_time = time.time()
        for instance in session.query(User).order_by(User.id):
            print(instance.name, instance.nickname)

        middle_time = time.time()
        print(start_time - middle_time)

        # 2
        for name, nickname in session.query(User.name, User.nickname).order_by(User.id):
            print(name, nickname)

        print(middle_time - time.time())
        # 걸리는 시간 비교 결과: 2번 방법이 더 빠름


def alias():
    with orm_session() as session:
        # ColumnElement.label() 사용으로 각 칼럼의 표현을 다르게 바꿀 수 있음
        for row in session.query(User.name.label('name_label')).all():
            print(row.name_label)

    with orm_session() as session:
        # User 같은 클래스 객체는 aliased 로 제어 가능
        from sqlalchemy.orm import aliased
        user_alias = aliased(User, name='user_alias')

        for row in session.query(user_alias, user_alias.name).all():
            print(row.user_alias)


def limit_and_offset():
    with orm_session() as session:
        # LIMIT과 OFFSET은 Python에서는 array slices와 ORDER_BY로 제어하는게 일반적
        for u in session.query(User).order_by(User.id)[1:3]:
            print(u)


if __name__ == '__main__':
    # get_list_query()
    # alias()
    limit_and_offset()
