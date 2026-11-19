from dataclasses import dataclass
from typing import Protocol


@dataclass
class Task:
    id: int
    title: str
    completed: bool = False


class TaskRepository(Protocol):

    def get_by_id(self, task_id: int) -> Task | None:
        ...

    def save(self, task: Task) -> None:
        ...


class InMemoryTaskRepository:

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}

    def get_by_id(self, task_id: int) -> Task | None:
        return self._tasks.get(task_id)

    def save(self, task: Task) -> None:
        self._tasks[task.id] = task
