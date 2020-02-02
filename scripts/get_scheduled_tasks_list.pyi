from typing_extensions import Literal
from scripts.get_scheduled_tasks_list import formats

def main(fmt: Literal[*formats]) -> None: ...
