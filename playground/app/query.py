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


def filter_and_filter_by():
    with orm_session() as session:
        start_time = time.time()

        # filter_by() : keyword arguments 사용
        name = session.query(User.name).filter_by(nickname='eddie')
        print(name)

        middle_time = time.time()
        print(middle_time - start_time)

        # filter() : SQL expression language 사용. 매핑한 클래스에서 정의한 속성 및 파이썬 연산자 사용 가능
        name = session.query(User.name).filter(User.nickname == 'eddie')
        print(name)

        print(time.time() - middle_time)
        # 걸리는 시간 비교 결과: 2번 방법이 더 빠름


def common_filter_op():
    with orm_session() as session:
        # Query 객체는 새로운 Query 객체 반환 => 이중 filter 가능
        check_time = time.time()
        name = session.query(User)\
            .filter(User.name == 'ed')\
            .filter(User.nickname == 'eddie')
        print(name)
        print(time.time() - check_time)

        # common operators used in filter()

        # ColumnOperators.__eq__() : equals
        check_time = time.time()
        print(session.query(User).filter(User.name == 'ed'))
        print(time.time() - check_time)

        # ColumnOperators.__ne__() : not equals
        check_time = time.time()
        print(session.query(User).filter(User.name != 'ed'))
        print(time.time() - check_time)

        # ColumnOperators.like() : like
        check_time = time.time()
        print(session.query(User).filter(User.name.like('%ed%')))
        print(time.time() - check_time)

        # like는 어떤 백엔드인지에 따라 case-sensitive 여부가 다름
        # case-insensitive를 위해서는 ColumnOperators.ilike()를 사용할 것
        # ColumnOperators.ilike() : case-insensitive like
        check_time = time.time()
        print(session.query(User).filter(User.name.ilike('%ed%')))
        print(time.time() - check_time)

        # ColumnOperators.in_() : in
        check_time = time.time()
        print(session.query(User).filter(User.name.in_(['ed', 'wendy', 'jack'])))
        print(time.time() - check_time)
        # 이중 쿼리도 가능
        check_time = time.time()
        print(session.query(User).filter(User.name.in_(
            session.query(User.name).filter(User.name.like('%ed%'))
        )))
        print(time.time() - check_time)

        # multi-column을 위한 tuple 사용 가능
        from sqlalchemy import tuple_
        check_time = time.time()
        print(session.query(User).filter(
            tuple_(User.name, User.nickname)
            .in_([('ed', 'eddie'), ('wendy', 'windy')])
        ))
        print(time.time() - check_time)

        # ColumnOperators.notin_(): not in
        check_time = time.time()
        print(session.query(User).filter(~User.name.in_(['ed', 'wendy', 'jack'])))
        print(time.time() - check_time)

        # ColumnOperators.is_() : is
        check_time = time.time()
        print(session.query(User).filter(User.name.is_(None)))
        print(time.time() - check_time)

        # ColumnOperators.isnot() : is not
        check_time = time.time()
        print(session.query(User).filter(User.name.isnot(None)))
        print(time.time() - check_time)

        # AND
        from sqlalchemy import and_
        check_time = time.time()
        print(session.query(User).filter(and_(User.name == 'ed', User.nickname == 'eddie')))
        print(session.query(User).filter(User.name == 'ed', User.nickname == 'eddie'))
        print(time.time() - check_time)

        # OR
        from sqlalchemy import or_
        check_time = time.time()
        print(session.query(User).filter(or_(User.name == 'ed', User.name == 'wendy')))
        print(time.time() - check_time)

        # ColumnOperators.match() : match
        check_time = time.time()
        print(session.query(User).filter(User.name.match('wendy')))
        print(time.time() - check_time)


def scalars():
    with orm_session() as session:
        check_time = time.time()
        # Query.first() : 가장 첫번째것을 반환
        print(session.query(User).first())
        print('first():', time.time() - check_time)
        # 만약 찾고자 하는 record가 없다면? -> None 반환
        check_time = time.time()
        print(session.query(User).filter(User.name == 'asdf').first())
        print(time.time() - check_time)

        # Query.one() : 해당 테이블의 모든 row를 fetch. 단 하나의 record가 있다면 반환
        check_time = time.time()
        print(session.query(User).filter(User.name == 'ed').one())
        print('one():', time.time() - check_time)
        # 2개 이상의 record가 있다면? -> sqlalchemy.orm.exc.MultipleResultsFound: Multiple rows were found for one()
        # print(session.query(User).one())
        # record가 하나도 없다면? -> sqlalchemy.orm.exc.NoResultFound: No row was found for one()
        # print(session.query(User).filter(User.id == 1000).one())

        # Query.one_or_none() : 해당하는 record가 하나있으면 반환 또는 없다면 None 반환
        check_time = time.time()
        print(session.query(User).filter(User.name == 'ed').one_or_none())
        print('one_or_none():', time.time() - check_time)
        # 2개 이상의 record가 있다면? -> sqlalchemy.orm.exc.MultipleResultsFound: Multiple rows were found for one_or_none()
        # print(session.query(User).one_or_none())
        # record가 하나도 없다면? -> None
        check_time = time.time()
        print(session.query(User).filter(User.id == 1000).one_or_none())
        print(time.time() - check_time)

        # Query.scalar() : Query.one을 호출하고 성공 시 첫번째 칼럼 반환
        check_time = time.time()
        print(session.query(User).filter(User.name == 'ed').scalar())
        print('scalar():', time.time() - check_time)
        # 2개 이상의 record가 있다면? -> sqlalchemy.orm.exc.MultipleResultsFound: Multiple rows were found for one()
        # print(session.query(User).scalar())
        # record가 하나도 없다면? -> None
        check_time = time.time()
        print(session.query(User).filter(User.id == 1000).scalar())
        print(time.time() - check_time)

        # 걸리는 시간 비교 결과: first()는 생각보다 느림. 나머지는 고만고만


if __name__ == '__main__':
    # get_list_query()
    # alias()
    # limit_and_offset()
    # filter_and_filter_by()
    # common_filter_op()
    scalars()
