import sqlite3


def delete_task(
        connection: sqlite3.Connection,
        task_id: int
) -> bool:
    _cursor = connection.execute(
        "DELETE FROM tasks WHERE id=?;",
        (task_id,)
    )

    return _cursor.rowcount == 1


if __name__ == '__main__':
    print('sqlite test')

    db_connection = sqlite3.connect("practice.db")

    try:
        with db_connection:
            db_connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    completed INTEGER NOT NULL DEFAULT 0
                );
                """
            )

            db_connection.execute(
                "INSERT INTO tasks (title) VALUES (?);",
                ("Learn SQLite",)
            )

            db_connection.execute(
                "UPDATE tasks SET completed=? WHERE id=?;",
                (1, 1)
            )

            delete_task(db_connection, 2)

        cursor = db_connection.execute(
            "SELECT id, title, completed FROM tasks ORDER BY id;"
        )

        for row in cursor:
            print(row)
    finally:
        db_connection.close()
