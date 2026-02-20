from typing import Optional


class UserService:
    def __init__(self):
        self.users: dict[str, dict[str, str]] = {}

    def create_user(self, user_id: str, name: str) -> dict[str, str]:
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        if user_id in self.users:
            raise ValueError("User already exists")
        self.users[user_id] = {"name": name.strip()}
        return self.users[user_id]

    def get_user(self, user_id: str) -> Optional[dict[str, str]]:
        return self.users.get(user_id)

    def delete_user(self, user_id: str) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
