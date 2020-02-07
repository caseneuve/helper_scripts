from typing import Optional

from typing_extensions import Literal

def main(
    command: str, hour: Optional[int], minute: int, disabled: Optional[Literal[True]]
) -> None: ...
