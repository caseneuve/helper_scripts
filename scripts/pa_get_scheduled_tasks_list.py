#!/usr/bin/python3.5
"""Get list of user's scheduled tasks.

Usage:
  pa_get_scheduled_tasks_list.py [--format=<format>]

Options:
  -h --help                      Print this message
  -f --format=<format>           Table format supported by tabulate
                                 (defaults to 'simple')
"""

import getpass

from docopt import docopt
from tabulate import tabulate

from pythonanywhere.task import TaskList


def main(fmt):
    attrs = "task_id", "interval", "printable_time", "enabled", "command"
    headers = "id", "interval", "at", "enabled", "command"
    table = [[getattr(task, attr) for attr in attrs] for task in TaskList().tasks]
    print(tabulate(table, headers, tablefmt=fmt))


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main(arguments.get("--format", "simple"))
