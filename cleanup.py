import json
from datetime import datetime
from pathlib import Path

DATE_FORMAT = "%d.%m.%Y.%H:%M"
DB_FILES = [
    Path("fish_users_v1.json"),
    Path("shaxta_users_v1.json"),
    Path("zavod_users_v1.json"),
    Path("fsin_users_v1.json"),
    Path("zal_users_v1.json"),
]

def load_users(db_file: Path):
    if not db_file.exists():
        return []

    with open(db_file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

def save_users(db_file: Path, users):
    with open(db_file, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def is_active(user):
    expires_at = user.get("expires_at", "")
    try:
        expire_date = datetime.strptime(expires_at, DATE_FORMAT)
        return expire_date > datetime.now()
    except ValueError:
        return False

def cleanup_file(db_file: Path):
    users = load_users(db_file)
    active_users = [user for user in users if is_active(user)]

    removed_count = len(users) - len(active_users)

    if users != active_users:
        save_users(db_file, active_users)

    print(f"{db_file.name}: удалено {removed_count}, осталось {len(active_users)}")

def main():
    for db_file in DB_FILES:
        cleanup_file(db_file)

if __name__ == "__main__":
    main()
