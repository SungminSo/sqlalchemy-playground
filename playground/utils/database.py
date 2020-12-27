from contextlib import contextmanager

from playground.models import Session


@contextmanager
def transaction():
    session = Session()
    try:
        yield session
        session.commit()
    except:  # noqa : # noqa가 있는 행은 linter 프로그램에 의해 무시됨.
        session.rollback()
        raise
    finally:
        session.close()


@contextmanager
def orm_session():
    session = Session()
    yield session

    session.close_all()
