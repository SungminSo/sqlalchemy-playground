from playground.models.users import User
from playground.utils.database import orm_session

if __name__ == '__main__':
    with orm_session() as session:
        ed_user = session.query(User).filter_by(name='ed').first()

        # revert 할 데이터
        ed_user.name = 'Edwardo'

        fake_user = User(name='fakeuser', nickname='fakeuser', password='qwerasdf', phone='010')
        session.add(fake_user)

        # 현재 transaction에 flush
        print(session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all())
        # [<User(name=Edwardo, nickname=eddie)>, <User(name=fakeuser, nickname=fakeuser)>]

        # 명시적 rollback
        session.rollback()

        print(ed_user.name)  # ed
        print(fake_user in session)  # False

        print(session.query(User).filter(User.name.in_(['ed', 'fakeuser'])).all())
        # [<User(name=ed, nickname=eddie)>]
