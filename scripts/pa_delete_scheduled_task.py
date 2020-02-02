#!/usr/bin/python3.5
"""Delete scheduled task.

Usage:
  pa_delete_scheduled_task.py <id>

Options:
  -h --help                      Print this message
"""

from docopt import docopt

from pythonanywhere.task import Task


def main(task_id):
    task = Task(task_id=task_id)
    task.delete_schedule()


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main(int(arguments["<id>"]))
