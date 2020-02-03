#!/usr/bin/python3.5
"""Delete scheduled task by id.

Usage:
  pa_delete_scheduled_task.py <id>

Options:
  -h --help                      Print this message

Note:
  Task <id> may be found using pa_get_scheduled_tasks_list.py script.
"""

from docopt import docopt
from schema import And, Schema, Use

from pythonanywhere.scripts_commons import validate_user_input
from pythonanywhere.task import Task


def main(task_id):
    task = Task.from_id(task_id=task_id)
    task.delete_schedule()


if __name__ == "__main__":
    schema = Schema({"<id>": And(Use(int), error="<id> must be an integer")})
    arguments = validate_user_input(docopt(__doc__), schema)

    main(int(arguments["<id>"]))
