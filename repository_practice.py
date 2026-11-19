from dataclasses import dataclass
from typing import Protocol


@dataclass
class Task:
    id: int
    title: str
    completed: bool = False


class TaskRepository(Protocol):

    def get_by_id(task_id: int) -> Task:
        ...

    def save(task: Task) -> None:
        ...
