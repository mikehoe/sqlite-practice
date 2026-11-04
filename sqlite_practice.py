import sqlite3


def delete_task(
        connection: sqlite3.Connection,
        task_id: int
) -> bool:
    cursor = connection.execute(
        "DELETE FROM tasks WHERE id=?;",
        (task_id,)
    )

    return cursor.rowcount == 1


def main() -> None:
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
                "INSERT INTO tasks (title) VALUES (?);",
                ("Learn SQLite",)
            )

            connection.execute(
                "UPDATE tasks SET completed=? WHERE id=?;",
                (1, 1)
            )
            task_id = 2
            deleted = delete_task(connection, task_id)
            print(f"Task {task_id} {'was' if deleted else 'was not'} deleted.")

        cursor = connection.execute(
            "SELECT id, title, completed FROM tasks ORDER BY id;"
        )

        for row in cursor:
            print(row)

    finally:
        connection.close()


if __name__ == '__main__':
    main()
