from ..models.users import User

ed_user = User(name='ed', nickname='ed_nickname', password='password', phone='01011112222')

print(ed_user.name)
print(ed_user.nickname)

print(ed_user)  # User __repr__로 정의한 형태로 나옴

print(ed_user.id)  # None. id는 __init__()에서 정의되지는 않았지만 매핑을 해뒀기 떄문에 None으로 존재. DB에 넣으면 id값은 알아서 들어옴
