import json
from datetime import datetime
from pathlib import Path

DB_FILE = Path("fish_users_v1.json")
DATE_FORMAT = "%d.%m.%Y.%H:%M"

def load_users():
    if not DB_FILE.exists():
        return []

    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

def save_users(users):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def is_active(user):
    expires_at = user.get("expires_at", "")
    try:
        expire_date = datetime.strptime(expires_at, DATE_FORMAT)
        return expire_date > datetime.now()
    except ValueError:
        return False

def main():
    users = load_users()
    active_users = [user for user in users if is_active(user)]

    if users != active_users:
        save_users(active_users)
        print(f"Удалено {len(users) - len(active_users)} просроченных записей")
    else:
        print("Просроченных записей нет")

if __name__ == "__main__":
    main()
