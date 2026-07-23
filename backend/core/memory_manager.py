import sqlite3


def save_message(username, role, content):

    db_path = f"../users/{username}/memory/chat_memory.db"

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chats (role, content)
        VALUES (?, ?)
        """,
        (role, content)
    )

    conn.commit()
    conn.close()

def get_last_messages(username, limit=10):

    db_path = f"../users/{username}/memory/chat_memory.db"

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM chats
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    messages = cursor.fetchall()

    conn.close()

    return messages[::-1]

def load_summary(username):
    try:
        with open(
            f"../users/{username}/memory/summary.txt",
            "r",
            encoding="utf-8"
        ) as f:
            return f.read()
    except:
        return ""


def save_summary(username, summary):

    import os

    memory_dir = f"../users/{username}/memory"

    os.makedirs(
        memory_dir,
        exist_ok=True
    )

    with open(
        f"{memory_dir}/summary.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(summary)


def count_messages(username):

    import sqlite3

    db_path = f"../users/{username}/memory/chat_memory.db"

    try:
        conn = sqlite3.connect(db_path)

        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM chats"
        )

        count = cursor.fetchone()[0]

        conn.close()

        return count

    except:
        return 0

