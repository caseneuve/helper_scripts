import logging
from typing import Dict, List, Optional

import schema

from pythonanywhere.task import Task

logger: logging.Logger = ...
tabulate_formats: List[str] = ...

class ScriptSchema(schema.Schema):
    boolean: schema.Or = ...
    hour: schema.Or = ...
    id_multi: schema.Or = ...
    id_required: schema.And = ...
    minute: schema.Or = ...
    minute_required: schema.And = ...
    string: schema.Or = ...
    tabulate_format: schema.Or = ...
    replacements: Dict[str] = ...
    def convert(self, string: str) -> str: ...
    def validate_user_input(self, arguments: dict, *, conversions: Optional[dict]) -> dict: ...

def get_logger(set_info: bool) -> logging.Logger: ...
def get_task_from_id(task_id: int, no_exit: bool) -> Task: ...
