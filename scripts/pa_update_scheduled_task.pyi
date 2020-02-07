from typing import Optional

from typing_extensions import Literal

def main(
    *,
    task_id: int,
    command: Optional[str],
    hour: Optional[int],
    minute: Optional[int],
    **kwargs: Optional[Literal[True]]
) -> None: ...
    def parse_opts(*opts: str) -> str: ...

