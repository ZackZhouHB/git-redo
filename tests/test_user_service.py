from src.user_service import UserService


def test_create_user():
    svc = UserService()
    user = svc.create_user("u1", "Alice")
    assert user["name"] == "Alice"


def test_get_user_not_found():
    svc = UserService()
    assert svc.get_user("nope") is None


def test_create_user_empty_name_raises():
    svc = UserService()
    try:
        svc.create_user("u2", "   ")
        assert False, "Expected ValueError for empty name"
    except ValueError as exc:
        assert str(exc) == "Name cannot be empty"


def test_delete_user():
    svc = UserService()
    svc.create_user("u3", "Bob")
    assert svc.delete_user("u3") is True
    assert svc.get_user("u3") is None
    assert svc.delete_user("u3") is False
