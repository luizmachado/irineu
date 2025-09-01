import os
import json

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register_user(user_id, username):
    users = load_users()
    if str(user_id) not in users:
        users[str(user_id)] = {
            "username": username,
            "authorized": False  # padrão: não autorizado
        }
        save_users(users)
    return users

def is_authorized(user_id):
    users = load_users()
    return users.get(str(user_id), {}).get("authorized", False)

