import sqlite3
from collections.abc import Iterator

import pytest

from sqlite_practice import delete_task


@pytest.fixture
def connection() -> Iterator[sqlite3.Connection]:
    db = sqlite3.connect(":memory:")
    try:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
            );
            """
        )
        yield db
    finally:
        db.close()


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
