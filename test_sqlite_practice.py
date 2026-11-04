import sqlite3
from collections.abc import Iterator

import pytest

from sqlite_practice import delete_task, create_task, get_task, list_tasks, update_task


@pytest.fixture
def connection() -> Iterator[sqlite3.Connection]:
    db = sqlite3.connect(":memory:")
    try:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL CHECK (length(trim(title)) > 0),
                completed INTEGER NOT NULL DEFAULT 0
            );
            """
        )
        yield db
    finally:
        db.close()


def test_create_task(connection: sqlite3.Connection) -> None:
    task_id = create_task(connection, "Learn SQLite")

    assert task_id == 1
    cursor = connection.execute(
        "SELECT id, title, completed FROM tasks WHERE id = ?",
        (task_id,)
    )
    assert cursor.fetchone() == (task_id, "Learn SQLite", 0)


def test_create_task_strips_whitespace(connection: sqlite3.Connection) -> None:
    task_id = create_task(connection, "  Learn SQLite  ")
    task = get_task(connection, task_id)
    assert task is not None
    assert task[1] == "Learn SQLite"


@pytest.mark.parametrize("title", ["", " ", "   ", "\t", "\n"])
def test_create_task_rejects_empty_title(connection: sqlite3.Connection,
                                         title: str) -> None:
    with pytest.raises(ValueError, match="Title cannot be empty"):
        create_task(connection, title)

    assert list_tasks(connection) == []


def test_direct_sql_insert_with_whitespaces(connection: sqlite3.Connection) -> None:
    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(
            "INSERT INTO tasks (title) VALUES (?);",
            ("   ",))

    assert list_tasks(connection) == []


def test_get_existing_task(connection: sqlite3.Connection) -> None:
    created_task_id = create_task(connection, "Learn SQLite")

    task = get_task(connection, created_task_id)
    assert task is not None

    retrieved_task_id, task_title, task_completed = task
    assert retrieved_task_id == created_task_id
    assert task_title == "Learn SQLite"
    assert task_completed == 0


def test_get_nonexistent_task(connection: sqlite3.Connection) -> None:
    task = get_task(connection, 999)
    assert task is None


def test_list_tasks_empty(connection: sqlite3.Connection) -> None:
    assert list_tasks(connection) == []


def test_list_tasks_ordered_by_id(connection: sqlite3.Connection) -> None:
    create_task(connection, "Learn SQLite")
    create_task(connection, "Learn Python")
    create_task(connection, "Run tests")

    assert list_tasks(connection) == [
        (1, "Learn SQLite", 0),
        (2, "Learn Python", 0),
        (3, "Run tests", 0)
    ]


def test_update_existing_task(connection: sqlite3.Connection) -> None:
    task_id = create_task(connection, "Learn SQLite")
    assert update_task(connection, task_id, "Run tests")

    task = get_task(connection, task_id)
    assert task is not None
    assert task[1] == "Run tests"


def test_update_nonexistent_task(connection: sqlite3.Connection) -> None:
    assert update_task(connection, 999, new_title="Run tests") is False


def test_update_task_strips_whitespace(connection: sqlite3.Connection) -> None:
    task_id = create_task(connection, "  Learn SQLite  ")
    assert update_task(connection, task_id, "  Run tests  ")

    task = get_task(connection, task_id)
    assert task is not None
    assert task[1] == "Run tests"


@pytest.mark.parametrize("title", ["", " ", "   ", "\t", "\n"])
def test_update_task_rejects_empty_title(connection: sqlite3.Connection,
                                         title: str) -> None:
    task_id = create_task(connection, "  Learn SQLite  ")
    with pytest.raises(ValueError, match="Title cannot be empty"):
        update_task(connection, task_id, title)

    assert get_task(connection, task_id) == (task_id, "Learn SQLite", 0)


def test_delete_existing_task(connection: sqlite3.Connection) -> None:
    connection.execute(
        "INSERT INTO tasks (title) VALUES (?);",
        ("Learn SQLite",)
    )
    connection.commit()
    assert delete_task(connection, 1)

    cursor = connection.execute(
        "SELECT id FROM tasks WHERE id = ?",
        (1,)
    )
    assert cursor.fetchone() is None


def test_delete_nonexistent_task(connection: sqlite3.Connection) -> None:
    assert delete_task(connection, 999) is False
