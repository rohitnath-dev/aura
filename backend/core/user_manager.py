import os
import json
import sqlite3


BASE_USERS_PATH = "../users"


def create_user(username):

    user_path = f"{BASE_USERS_PATH}/{username}"

    raw_path = f"{user_path}/raw_data"

    processed_path = f"{user_path}/processed_data"

    memory_path = f"{user_path}/memory"

    # create folders
    os.makedirs(raw_path, exist_ok=True)
    os.makedirs(processed_path, exist_ok=True)
    os.makedirs(memory_path, exist_ok=True)

    # create memory db
    db_path = f"{memory_path}/chat_memory.db"

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT,
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

    print(f"{username} initialized")

def save_profile(username, profile_data):

    profile_path = f"{BASE_USERS_PATH}/{username}/raw_data/profile.json"

    with open(profile_path, "w") as f:
        json.dump(profile_data, f, indent=4)
