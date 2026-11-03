import sqlite3

if __name__ == '__main__':
    print('sqlite test')

    connection = sqlite3.connect("practice.db")

    try:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    completed INTEGER NOT NULL DEFAULT 0
                );
                """
            )

            connection.execute(
                "INSERT INTO tasks (title) VALUES (?)",
                ("Learn SQLite",)
            )

        cursor = connection.execute(
            "SELECT id, title, completed FROM tasks ORDER BY id;"
        )

        for row in cursor:
            print(row)
    finally:
        connection.close()
