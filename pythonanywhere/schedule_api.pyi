from typing import Optional

from typing_extensions import TypedDict

class Params(TypedDict):
    command: str
    enabled: bool
    hour: int
    interval: str
    minute: int

class Schedule:
    base_url: str = ...
    def __init__(self) -> None: ...
    def create(self, params: Params) -> Optional[dict]: ...
    def delete(self, task_id: int) -> None: ...
