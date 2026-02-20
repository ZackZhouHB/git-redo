from src.user_service import UserService


def test_create_user():
    svc = UserService()
    user = svc.create_user("u1", "Alice")
    assert user["name"] == "Alice"


def test_get_user_not_found():
    svc = UserService()
    assert svc.get_user("nope") is None
