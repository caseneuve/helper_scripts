#!/usr/bin/python3.5
"""Delete scheduled task.

Usage:
  pa_delete_scheduled_task.py <id>

Options:
  -h --help                      Print this message
"""

from docopt import docopt
from schema import Schema

from pythonanywhere.task import Task


def main(task_id):
    task = Task(task_id=task_id)
    task.delete_schedule()


if __name__ == "__main__":
    schema = Schema({"<id>": And(int, error="<id> must be an integer")})
    arguments = validate_user_input(docopt(__doc__), schema)

    main(int(arguments["<id>"]))
