import sqlite3


def create_task(connection: sqlite3.Connection, title: str) -> int:
    cursor = connection.execute(
        "INSERT INTO tasks (title) VALUES (?)",
        (title,)
    )
    task_id = cursor.lastrowid

    if task_id is None:
        raise RuntimeError("Failed to retrieve the new task ID")

    return task_id


def get_task(connection: sqlite3.Connection,
             task_id: int) -> tuple[int, str, int] | None:
    cursor = connection.execute(
        "SELECT id, title, completed FROM tasks WHERE id=?;",
        (task_id,)
    )
    return cursor.fetchone()


def list_tasks(connection: sqlite3.Connection) -> list[tuple[int, str, int]]:
    cursor = connection.execute(
        "SELECT id, title, completed FROM tasks ORDER BY id;"
    )
    return cursor.fetchall()


def update_task(connection: sqlite3.Connection, task_id: int,
                new_title: str) -> bool:
    cursor = connection.execute(
        "UPDATE tasks SET title=? WHERE id=?;",
        (new_title, task_id)
    )

    return cursor.rowcount == 1


def delete_task(connection: sqlite3.Connection, task_id: int) -> bool:
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

            task_title = "Learn SQLite"
            task_id = create_task(connection, task_title)
            print(f"Task '{task_title}' with id={task_id} was created.")

            new_title = "Test SQLite"
            updated = update_task(connection, task_id, new_title)
            if updated:
                print(f"Task {task_title} was updated to {new_title}.")
            else:
                print(f"Task {task_title} was not updated.")

            task_id = 2
            deleted = delete_task(connection, task_id)
            print(f"Task {task_id} {'was' if deleted else 'was not'} deleted.")

        tasks = list_tasks(connection)

        for task in tasks:
            print(task)

    finally:
        connection.close()


if __name__ == '__main__':
    main()
