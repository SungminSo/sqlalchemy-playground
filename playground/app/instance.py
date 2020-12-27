from playground.models.users import User
from playground.utils.database import orm_session

if __name__ == '__main__':
    ed_user = User(name='ed', nickname='ed_nickname', password='password', phone='01011112222')

    print(ed_user.name)  # ed
    print(ed_user.nickname)  # ed_nickname

    print(ed_user)  # User __repr__로 정의한 형태로 나옴. <User(name=ed, nickname=ed_nickname)>

    print(ed_user.id)  # None. id는 __init__()에서 정의되지는 않았지만 매핑을 해뒀기 떄문에 None으로 존재. DB에 넣으면 id값은 알아서 들어옴

    with orm_session() as session:
        session.add(ed_user)  # pending.
        # 아직 DB에 저장되지는 않은 상태인데 flush 과정을 통해 입력됨

        # query를 실행하면 pending 되어있는 데이터들이 flush된 후에 쿼리 실행
        # 이때 fluash된 데이터들은 실제 저장된 것은 아님
        query_user = session.query(User).filter_by(name='ed').first()
        print(query_user)  # <User(name=ed, nickname=ed_nickname)>
        print(ed_user is query_user)  # True
        print(query_user.id)  # None이 아님
        # 실행 완료 후 sqlalchemy.engine.base.Engine ROLLBACK

        # 한번에 여러 객체 저장
        session.add_all([
            User(name='wendy', nickname='windy', password='password', phone='01022223333'),
            User(name='mary', nickname='mary', password='password', phone='01033334444'),
            User(name='fred', nickname='freddy', password='password', phone='01044445555'),
        ])

        # flush 된 데이터 변경이 있을 시 dirty로 체크
        ed_user.nickname = 'eddie'
        print(session.dirty)  # IdentitySet([<User(name=ed, nickname=eddie)>])

        # flush 되기 전 데이터는 new로 체크
        print(session.new)  # IdentitySet([<User(name=wendy, nickname=windy)>, <User(name=mary, nickname=mary)>, <User(name=fred, nickname=freddy)>])

        # flush & commits transaction
        session.commit()

        # sqlalchey refresh data and access within a new transaction
        print(ed_user.id)
